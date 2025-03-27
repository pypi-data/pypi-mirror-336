import os
import io
import requests
import logging
import warnings
from pathlib import Path

import pandas as pnd
import gempipe
import cobra



def get_expcon(logger):
    
    
    logger.info("Downloading the excel file...")
    sheet_id = "1qGbIIipHJgYQjk3M0xDWKvnTkeInPoTeH9unDQkZPwg"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
    response = requests.get(url)  # download the requested file
    if response.status_code == 200:
        excel_data = io.BytesIO(response.content)   # load into memory
        exceldb = pnd.ExcelFile(excel_data)
    else:
        logger.error(f"Error during download. Please contact the developer.")
        return 1
    
    
    # check table presence
    sheet_names = exceldb.sheet_names
    for i in ['media', 'PM1', 'PM2', 'PM3', 'PM4', 'authors']: 
        if i not in sheet_names:
            logger.error(f"Sheet '{i}' is missing!")
            return 1
        
        
    # load the tables
    expcon = {}
    expcon['media'] = exceldb.parse('media')
    expcon['PM1'] = exceldb.parse('PM1')
    expcon['PM2'] = exceldb.parse('PM2')
    expcon['PM3'] = exceldb.parse('PM3')
    expcon['PM4'] = exceldb.parse('PM4')
    expcon['authors'] = exceldb.parse('authors')
    
    
    # assign substrates as index
    expcon['media'].index = expcon['media'].iloc[:, 1]
    # remove first 2 useless column (empty & substrates)
    expcon['media'] = expcon['media'].iloc[:, 2:]
    

    return expcon

       

def check_inputs(logger, universe, eggnog):
    
    
    # check if files exist
    if os.path.isfile(universe) == False: 
        logger.error(f"Provided --universe doesn't exist: {universe}.")
        return 1
    if os.path.isfile(eggnog) == False: 
        logger.error(f"Provided --eggnog doesn't exist: {eggnog}.")
        return 1
    
    
    # check the universe model format
    if universe.endswith('.xml'):
        universe = cobra.io.read_sbml_model(universe)
    else: 
        logger.error(f"Provided --universe must be in cobrapy-compatible SBML format (.xml extension).")
        return 1
    
    
    # log main universe metrics:
    oG = len([g.id for g in universe.genes])
    R = len([r.id for r in universe.reactions if len(set([m.id.rsplit('_',1)[-1] for m in r.metabolites]))==1])
    T = len([r.id for r in universe.reactions if len(set([m.id.rsplit('_',1)[-1] for m in r.metabolites]))!=1])
    M = len([m.id for m in universe.metabolites])
    uM = len(set([m.id.rsplit('_', 1)[0] for m in universe.metabolites]))
    gr = len([gr.id for gr in universe.groups])
    bP = len([m.id for m in universe.reactions.get_by_id('Biomass').reactants])
    logger.info(f"Provided universe: [oG: {oG}, R: {R}, T: {T}, uM: {uM}, gr: {gr}, bP: {bP}, Biomass: {round(universe.slim_optimize(), 3)}]")
        
        
    # load eggnog annotations
    eggnog = pnd.read_csv(eggnog, sep='\t', comment='#', header=None)
    eggnog.columns = 'query	seed_ortholog	evalue	score	eggNOG_OGs	max_annot_lvl	COG_category	Description	Preferred_name	GOs	EC	KEGG_ko	KEGG_Pathway	KEGG_Module	KEGG_Reaction	KEGG_rclass	BRITE	KEGG_TC	CAZy	BiGG_Reaction	PFAMs'.split('\t')
    eggnog = eggnog.set_index('query', drop=True, verify_integrity=True)
    
    return [universe, eggnog]



def parse_eggnog(eggnog):
    
    
    # PART 1. get KO codes available
    gid_to_kos = {}
    ko_to_gids = {}
    for gid, kos in eggnog['KEGG_ko'].items():
        if kos == '-': 
            continue
            
        if gid not in gid_to_kos.keys(): 
            gid_to_kos[gid] = set()
            
        kos = kos.split(',')
        kos = [i.replace('ko:', '') for i in kos]
        for ko in kos: 
            if ko not in ko_to_gids.keys(): 
                ko_to_gids[ko] = set()
                
            # populate dictionaries
            ko_to_gids[ko].add(gid)
            gid_to_kos[gid].add(ko)

    
    return ko_to_gids, gid_to_kos



def get_modeled_kos(model):
    
    
    # get modeled KO ids:
    modeled_gid_to_ko = {}
    modeled_ko_to_gid = {}
    
    for g in model.genes:
        if g.id in ['orphan', 'spontaneous']: 
            continue
        corresponding_ko = g.annotation['ko']
        
        modeled_gid_to_ko[g.id] = corresponding_ko
        modeled_ko_to_gid[corresponding_ko] = g.id
        
    modeled_kos = list(modeled_gid_to_ko.values())
        
    return modeled_kos, modeled_gid_to_ko, modeled_ko_to_gid



def subtract_kos(logger, model, eggonog_ko_to_gids):
    
    
    modeled_kos, _, modeled_ko_to_gid = get_modeled_kos(model)
        
        
    to_remove = []  # genes to delete
    for ko in modeled_kos: 
        if ko not in eggonog_ko_to_gids.keys():
            gid_to_remove = modeled_ko_to_gid[ko]
            to_remove.append(model.genes.get_by_id(gid_to_remove))
            
    
    # remove also orphan reactions!
    to_remove.append(model.genes.get_by_id('orphan'))
    
    
    # delete marked genes!
    # trick to avoid the WARNING "cobra/core/group.py:147: UserWarning: need to pass in a list" 
    # triggered when trying to remove reactions that are included in groups. 
    with warnings.catch_warnings():  # temporarily suppress warnings for this block
        warnings.simplefilter("ignore")  # ignore all warnings
        cobra_logger = logging.getLogger("cobra.util.solver")
        old_level = cobra_logger.level
        cobra_logger.setLevel(logging.ERROR)   

        cobra.manipulation.delete.remove_genes(model, to_remove, remove_reactions=True)

        # restore original behaviour: 
        cobra_logger.setLevel(old_level)   
        
   
    logger.info(f"Found {len(model.genes)} modeled orthologs.")
    return 0



def translate_remaining_kos(logger, model, eggonog_ko_to_gids):
    
    
    _, modeled_gid_to_ko, _ = get_modeled_kos(model) 
    
    
    # iterate reactions:
    for r in model.reactions:

        gpr = r.gene_reaction_rule

        # force each gid to be surrounded by spaces: 
        gpr = ' ' + gpr.replace('(', ' ( ').replace(')', ' ) ') + ' '
        
        for gid in modeled_gid_to_ko.keys():
            if f' {gid} ' in gpr:
                
                new_gids = eggonog_ko_to_gids[modeled_gid_to_ko[gid]]
                gpr = gpr.replace(f' {gid} ', f' ({" or ".join(new_gids)}) ')       
            

        # remove spaces between parenthesis
        gpr = gpr.replace(' ( ', '(').replace(' ) ', ')')
        # remove spaces at the extremes: 
        gpr = gpr[1: -1]


        # New genes are introduced. Parethesis at the extremes are removed if not necessary. 
        r.gene_reaction_rule = gpr
        r.update_genes_from_gpr()
            
            
    # remaining old 'Cluster_'s need to removed.
    # remove if (1) hte ID starts with clusters AND (2) they are no more associated with any reaction
    to_remove = []
    for g in model.genes:
        
        if g.id in ['orphan', 'spontaneous']:
            continue
            
        if g.id in modeled_gid_to_ko.keys() and len(g.reactions)==0:
            to_remove.append(g)
            
    # warning suppression not needed here, as no reaction is actually removed.
    cobra.manipulation.delete.remove_genes(model, to_remove, remove_reactions=True)
    
        
    logger.info(f"Translated orthologs to {len(model.genes)} genes.")
    return 0
        
    
    
def include_forced(logger, model, universe, force_inclusion):
    
    if force_inclusion != '-':
        forced_rids = force_inclusion.split(',')
        
        modeled_rids = [r.id for r in model.reactions]
        universal_rids = [r.id for r in universe.reactions]
        
        introduced_rids = []
        for rid in forced_rids: 
            
            if rid not in universal_rids:
                logger.info(f"Ignoring reaction ID {rid} since it's not included in the universe.")
                continue
            
            if rid not in modeled_rids:
                gempipe.import_from_universe(model, universe, rid)
                introduced_rids.append(rid)
            else:
                logger.debug(f"Requested reaction ID {rid} was already included.")
        logger.info(f"Reactions forcibly included and orphans: {introduced_rids}.")
        
    return 0



def gapfill_on_media(logger, model, universe, expcon, media):
    
    if media == '-':
        logger.info(f"No media provided: gap-filling will be skipped.")
        return 0
    media = media.split(',')
    
    
    # at least 1 medium must exist
    if any([i in expcon['media'].columns for i in media])==False:
        logger.error(f"None of the provided media IDs exist. Available media are {list(expcon['media'].columns)}.")
        return 1
        
    
    def apply_medium(logger, model, medium, column):
        
        # retrieve metadata
        description = column.iloc[0]
        doi = column.iloc[1]
        author = column.iloc[2]
        units = column.iloc[3]
        
        # covert to dict
        column = column.iloc[4:]
        column = column.to_dict()
        
        # add trace elements:
        column['fe2'] = 'NL'
        column['mobd'] = 'NL'
        column['cobalt2'] = 'NL'
        
        
        # reset exchanges
        gempipe.reset_growth_env(model)    
        modeled_rids = [r.id for r in model.reactions]

        
        for substrate, value in column.items():

            if type(value)==float:
                continue   # empty cell, exchange will remain close
                        
            # check if exchange is modeled
            if f'EX_{substrate}_e' not in modeled_rids:
                logger.error(f"No exchange reaction found for substrate '{substrate}' in medium '{medium}'.")
                return 1
            
            
            value = value.strip().rstrip()
            if value == 'NL':   # non-limiting case
                model.reactions.get_by_id(f'EX_{substrate}_e').lower_bound = -1000
                    
                    
            elif '+-' not in value and '±' not in value:  # single number case
                value = value.replace(' ', '')  # eg "- 0.01" --> "-0.01"
                try: value = float(value)
                except: 
                    logger.error(f"Invalid value found in medium '{medium}': '{substrate}' {value}.")
                    return 1
                model.reactions.get_by_id(f'EX_{substrate}_e').lower_bound = value
                
                
            else:  # value & experimental error case
                if '±' in value: 
                    value, error = value.split('±', 1)
                else: value, error = value.split('+-', 1)
                value = value.rstrip()
                error = error.strip()
                value = value.replace(' ', '')  # eg "- 0.01" --> "-0.01"
                try: value = float(value)
                except: 
                    logger.error(f"Invalid value found in medium '{medium}': '{substrate}' {value} +- {error}.")
                    return 1
                try: error = float(error)
                except: 
                    logger.error(f"Invalid value found in medium '{medium}': '{substrate}' {value} +- {error}.")
                    return 1
                model.reactions.get_by_id(f'EX_{substrate}_e').lower_bound = value -error
                model.reactions.get_by_id(f'EX_{substrate}_e').upper_bound = value +error
            
        return 0
        
    
    def verify_growth(model):
        
        res = model.optimize()
        obj_value = res.objective_value
        status = res.status
        if obj_value < 0.001 or status=='infeasible':
            return False
        else: return True
        
        
    # make an editable copy:
    repository_nogenes = universe.copy()
    # remove genes to avoid the "ValueError: id purP is already present in list"
    cobra.manipulation.delete.remove_genes(repository_nogenes, [g.id for g in repository_nogenes.genes], remove_reactions=False)
    
    # get biomass mprecursors to gapfill:
    biomass_mids = set([m.id for m in universe.reactions.Biomass.metabolites])
    # remove GAM components:
    biomass_mids = biomass_mids - set(['atp_c', 'h2o_c', 'adp_c', 'h_c', 'pi_c'])
    # put atp_c as first:
    biomass_mids = ['atp_c'] + list(biomass_mids)
    # TMP
    biomass_mids = [
        'atp_c', 'ctp_c', 'gtp_c', 'utp_c', # ribo_nucleotides
        'datp_c', 'dctp_c', 'dgtp_c', 'dttp_c', # deoxyribo_nucleotides
        # amino_acids
        'ala__L_c', 'arg__L_c', 'asn__L_c', 'asp__L_c', 'cys__L_c', 
        'gln__L_c', 'glu__L_c', 'gly_c',    'his__L_c', 'ile__L_c', 
        'leu__L_c', 'lys__L_c', 'met__L_c', 'ser__L_c', 'pro__L_c', 
        'thr__L_c', 'trp__L_c', 'tyr__L_c', 'val__L_c', 'phe__L_c',
        # cofactors
        'accoa_c', 
        'nad_c', 'nadp_c', 
        'fmn_c', 'fad_c', 
        'moco_c',  # molybdenum cofactor
        'thf_c',   # tetrahydrofolate
        'thmpp_c',   # thiamine-pp
        'pydx5p_c', # vitamin B6 (pyridoxal 5-phosphate)
        'ribflv_c',  # riboflavin
        'pnto__R_c',  # pantothenate
        'mql8_c', # menaquinol / manaquinone (mqn8_c)
        'q8h2_c', # ubiquinol / ubiquinone (q8_c)
        'phllqol_c', # phylloquinol / phylloquinone (phllqne_c)
        'btn_c', # biotin
        'adocbl_c', # vitamin B12
        'hemeO_c', # heme O
        'pheme_c', # protoheme
        'sheme_c', # siroheme
        'gthrd_c', # glutathione (reduced)
        # membrane_wall
        'pe120_c', # phosphatidyl-ethanolamine (12:0;12:0)
        'pg120_c', # phosphatidyl-glycerol (12:0;12:0)
        'clpn120_c', # cardiolipin (12:0;12:0;12:0;12:0)
        'peptido_c', # peptidoglycan 
        'udcpdp_c', # undecaprenyl diphosphate (plantarum)
        'WTAgg40r_20n_20a_P_c', # teichoic acids
        'WTArg40r_20g_20a_P_c', # teichoic acids
        'WTAg40g_20g_20a_P_c', # teichoic acids
        'LTAgg40g_20n_20a_c', # lipoteichoic acids
        'LTAga40g_20t_20a_c', # lipoteichoic acids            
        # 1-lysyl phosphatidylglycerol (plantarum)
        # capsular polysaccharides
        
    ]
        
    for medium in media: 
        
        if medium not in expcon['media'].columns:
            logger.info(f"Medium '{medium}' does not exists and will be ignored.")
            continue
        
        
        response = apply_medium(logger, universe, medium, expcon['media'][medium])
        if response == 1: return 1

        if not verify_growth(universe):
            logger.error(f"Medium '{medium}' does not support growth of universe.")
            return 1

        response = apply_medium(logger, model, medium, expcon['media'][medium])
        if response == 1: return 1

        if verify_growth(model):
            logger.info(f"No need to gapfill model on medium '{medium}'.")
            continue



        # launch gap-filling separately for each biomass precursor:
        for mid in biomass_mids:
            
            if gempipe.can_synth(model, mid)[0]:
                logger.debug(f"Gap-filled 0 reactions on medium '{medium}' for '{mid}': [].")
                continue   # save time!
            suggested_rids = gempipe.perform_gapfilling(model, repository_nogenes, mid, nsol=1, verbose=False)
            logger.debug(f"Gap-filled {len(suggested_rids)} reactions on medium '{medium}' for '{mid}': {suggested_rids}.")
            for rid in suggested_rids:
                gempipe.import_from_universe(model, repository_nogenes, rid)
                
                
    
    return 0
    

    
    
def check_biosynthesis(logger, model, universe, growth, biosynth, reference, exclude_orphans):
    
    
    if growth: 
        
        # check production of biomass precursors: 
        logger.info("Checking biosynthesis of every biomass component...")
        
        print()
        mids = gempipe.check_reactants(model, 'Biomass')
        if mids == []: 
            print("No blocked biomass component detected!")
        print()

        
        
    if biosynth != '-':
        
        # check biosynthesis of every modeled metabolite:
        logger.info("Checking biosynthesis of every metabolite...")
        df_rows = []
        for m in model.metabolites:
            if m.id.endswith('_c'):
                binary, obj_value, status = gempipe.can_synth(model, m.id)
                df_rows.append({'mid': m.id, 'binary': binary, 'obj_value': obj_value, 'status': status})
        df_rows = pnd.DataFrame.from_records(df_rows)
        df_rows = df_rows.set_index('mid', drop=True, verify_integrity=True)
        
        # save table as excel: 
        df_rows.to_excel('biosynth.xlsx')
        logger.info(f"'{os.getcwd()}/biosynth.xlsx' created!")
        
        
        
        # focus on a particular metabolite:
        modeld_mids = [m.id for m in model.metabolites]
        if not (biosynth in modeld_mids and biosynth.endswith('_c')):
            logger.error(f"Cytosolic metabolite defined with --biosynth is not included: '{biosynth}'.")
            return 1
        
        nsol = 5   # number of solutions
        logger.info(f"Computing {nsol} gapfilling solutions for cytosolic metabolite {biosynth}...")

        
        # if provided, use the reference model as repository of reactions
        if reference != '-':   
            if reference.endswith('.xml'):
                refmodel = cobra.io.read_sbml_model(reference)
            elif reference.endswith('.json'):
                refmodel = cobra.io.load_json_model(reference)
            else:
                logger.error(f"Likely unsupported format found in --reference. Please use '.xml' or '.json'.")
                return 1
            repository = refmodel
        else:
            repository = universe
            

        # make an editable copy:
        repository_nogenes = repository.copy()
        
        
        if exclude_orphans:
            logger.info(f"Gapfilling is performed after removing orphan reactions.")
            to_remove = []
            
            cnt = 0
            for r in repository_nogenes.reactions: 
                if len(r.genes) !=0:
                    continue 
                if len(r.metabolites) ==1:
                    continue   # exclude exchanges/sinks/demands
                if any([m.id.endswith('_e') for m in r.metabolites]):
                    continue   # exclude transporters
                
                cnt +=1
                to_remove.append(r)
                logger.debug(f"Removing orphan #{cnt}: {r.id} ({r.reaction}).")
            repository_nogenes.remove_reactions(to_remove)
        
        
        # remove genes to avoid the "ValueError: id purP is already present in list"
        cobra.manipulation.delete.remove_genes(repository_nogenes, [g.id for g in repository_nogenes.genes], remove_reactions=False)
        
        
        # model and universe are already set up with the same growth medium:
        print()
        # perform gap-filling, solutions are shown using print()
        _ = gempipe.perform_gapfilling(model, repository_nogenes, biosynth, nsol=nsol)
        print()
             
    
    return 0

    

def unipruner(args, logger): 
        
    
    # check input files:
    response = check_inputs(logger, args.universe, args.eggnog)
    if type(response)==int:
        return 1
    universe = response[0]
    eggnog = response[1]
    
    
    # check file structure
    expcon = get_expcon(logger)
    if type(expcon)==int: return 1
    
    
    # get important dictionaries: 'eggnog_ko_to_gids' and 'eggonog_gid_to_kos'
    eggnog_ko_to_gids, eggonog_gid_to_kos = parse_eggnog(eggnog)
    
    
    # make a copy
    model = universe.copy()
    model.id = Path(args.eggnog).stem 
    
            
    # substract missing KOs
    subtract_kos(logger, model, eggnog_ko_to_gids)
    translate_remaining_kos(logger, model, eggnog_ko_to_gids)
    
    
    # force inclusion of reactions:   [[SHOULD BE LOGGED]]
    include_forced(logger, model, universe, args.force_inclusion)
    
    
    # gap-fill based on media:
    response = gapfill_on_media(logger, model, universe, expcon, args.media)
    if response==1: return 1
    
    
    # output the model:
    cobra.io.save_json_model(model, f'{model.id}.json')
    cobra.io.write_sbml_model(model, f'{model.id}.xml')   # groups are saved only to SBML 
    G = len([g.id for g in model.genes])
    R = len([r.id for r in model.reactions if len(set([m.id.rsplit('_',1)[-1] for m in r.metabolites]))==1])
    T = len([r.id for r in model.reactions if len(set([m.id.rsplit('_',1)[-1] for m in r.metabolites]))!=1])
    M = len([m.id for m in model.metabolites])
    uM = len(set([m.id.rsplit('_', 1)[0] for m in model.metabolites]))
    gr = len([gr.id for gr in model.groups])
    bP = len([m.id for m in model.reactions.get_by_id('Biomass').reactants])
    logger.info(f"'{os.getcwd()}/{model.id}.json' created!")
    logger.info(f"'{os.getcwd()}/{model.id}.xml' created!")
    logger.info(f"Resulting model: [G: {G}, R: {R}, T: {T}, uM: {uM}, gr: {gr}, bP: {bP}, Biomass: {round(model.slim_optimize(), 3)}]")
    
    
    response = check_biosynthesis(logger, model, universe, args.growth, args.biosynth, args.reference, args.exclude_orphans)
    if response==1: return 1

    
    return 0