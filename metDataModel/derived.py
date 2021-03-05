"""
Classes derived from the 8 basic classes.

# ideas to consider
class mzCompound(Compound):
    '''
    Not used now. Possibly intermediate format

    Ions are precomputed as a dictionary.
        Take into consideration of charge state; adjust adduct calculation based on charge

    '''
    'peaks': {
                'M+H[1+]': 0,
                'M[1+]': 0,
                'M+Na[1+]': 0,
                #
                'M-H[1-]': 0,
                'M-H2O-H[-]': 0,
                'M-2H[2-]': 0,
            },
    
    self.inferred_formula = ''
    self.class = ''  # refer to Classifire ontology or lipid ontology

# not necessary, simple lists will do:
class metaboliteSet:
    self.members = []
class similarityGroup:
    self.members = []


compound example in mummichog 2: 
'formula': 'C45H70N7O18P3S', 'mw': 1121.3710887012, 'name': '3(S)-hydroxy-tetracosa-12,15,18,21-all-cis-tetraenoyl-CoA', 
'adducts': {'M+K[1+]': 1160.33386516797, 'M+Cl[-]': 1156.3399887012001, 'M+Br[-]': 1200.2893887012, 'M+H[1+]': 1122.37836516797, 'M+HCOOK[1+]': 1206.33966516797, 'M(C13)+3H[3+]': 375.13203936717, 'M+ACN-H[-]': 1161.39035723443, 'M+Cl37[-]': 1158.3369887012, 'M-H2O-H[-]': 1102.35321223443, 'M(S34)+H[1+]': 1124.37416516797, 'M+CH3COO[-]': 1180.3843837012, 'M[1+]': 1121.3710887012, 'M-HCOOH+H[1+]': 1076.37296516797, 'M+NaCl[1+]': 1180.33696516797, 'M+H+Na[2+]': 572.68382081737, 'M+H2O+H[1+]': 1140.3889651679701, 'M-H+O[-]': 1136.35872223443, 'M+K-2H[-]': 1157.31203576766, 'M+2H[2+]': 561.69282081737, 'M+Br81[-]': 1202.2873887012001, 'M-H2O+H[1+]': 1104.36776516797, 'M-C3H4O2+H[1+]': 1050.3572651679701, 'M-NH3+H[1+]': 1105.3518651679701, 'M+Na-2H[-]': 1141.33853576766, 'M-CO2+H[1+]': 1078.38856516797, 'M+Na[1+]': 1144.36036516797, 'M-2H[2-]': 559.67826788383, 'M-H4O2+H[1+]': 1086.3571651679702, 'M(C13)-H[-]': 1121.36721223443, 'M(C13)+2H[2+]': 562.1945208173701, 'M(S34)-H[-]': 1122.35961223443, 'M+HCOO[-]': 1166.3687337012, 'M-H[-]': 1120.36381223443, 'M+HCOONa[1+]': 1190.36576516797, 'M+3H[3+]': 374.79763936717, 'M(C13)+H[1+]': 1123.3817651679701, 'M-CO+H[1+]': 1094.3833651679702}


"""

from metDataModel.core import Experiment, Compound

class metabolicModel:
    '''
    A metabolic model, minimal information is list_of_reactions.
    Pathway definition isn't always available.
    Compounds are union of all reactants and products in reactions.
    Genes and proteins correspond to enzymes in reactions.
    '''
    species = ''
    source = ''                 # where the model comes from
    version = ''

    list_of_reactions = []      # using core.Reaction 
    list_of_pathways = []

    # these can be derived from Reactions 
    list_of_compounds = []
    network = None


class userData(Experiment):
    '''
    If no annotation is given, 
    the data should be list_of_features.
    list_of_empCpds is generated by annotation methods.
    '''
    meta_data = {}              # from Experiment attributes
    list_of_empCpds = []
    list_of_features = []


class MS2feature(Feature):
    ms_level = 2
    parent_ion = 0

    list_mz = []
    list_intensity = []
    retention_time = 0


class annotatedCompound(EmpiricalCompound):
    '''
    Class for annotated compounds, which can have annotation from authentic standards, MS^n or other information.
    library compound will use same class

    We will have a cumulative list of annotatedCompound
    libraryCompound = annotatedCompound
    '''
    observed_mass = 0.0000


class Compound_spectra(Compound):
    '''
    Compound with added spectra from spectral databases or in silico prediciton.
    Refer to how HMDB organizes spectra for metabolites.
    '''
    meta = {}
    MS1_ESI_pos = []
    MS1_ESI_neg = []
    MS1_EISA_pos = []
    MS1_EISA_neg = []
    MS1_GC_pos = []
    MS1_GC_neg = []
    MS2_CID_pos = []
    MS2_CID_neg = []


class Contaminant(Compound):
    '''
    A class for common contaminants according to manufacturers or community. E.g.
    https://github.com/stanstrup/commonMZ
    ion_ID	mz	ion_type	molecular_formula	compound_ID	origin	ESI	MALDI	references
    1	33.03349	[M+H]+	CH3OH	Methanol	Acetonitrile, solvent	X		A
    2	42.03383	[M+H]+	CH3CN	ACN	Acetonitrile, solvent	X		A
    3	59.06037	[M+NH4]+	CH3CN	ACN	Acetonitrile, solvent	X		A, F

    https://www.maconda.bham.ac.uk/
    name	formula	exact_mass	std_inchi	std_inchi_key	id	type_of_contaminant	pubchem_cid	reference	ion_mode	mz	exact_adduct_mass	ion_form	instrument_type	instrument	chromatography	ion_source_type
    Acetic Acid	C2H4O2	60.02113	InChI=1S/C2H4O2/c1-2(3)4/h1H3,(H,3,4)	QTBSBXVTEAMEQO-UHFFFAOYSA-N	CON00001	Solvent	176	Tong, H., Bell, D., Tabei, K., & Siegel, M. M. (1999). Automated data massaging, interpretation, and E-mailing modules for high throughput open access mass spectrometry. Journal of the American Society for Mass Spectrometry, 10(11), 1174-1187, doi:10.1016/s1044-0305(99)00090-2.	NEG	59	59.0138536	[M-H]-	Ion trap	Micromass Platform II	LC	ESI
    Acetic Acid	C2H4O2	60.02113	InChI=1S/C2H4O2/c1-2(3)4/h1H3,(H,3,4)	QTBSBXVTEAMEQO-UHFFFAOYSA-N	CON00001	Solvent	176	Ijames, C. F., Dutky, R. C., & Fales, H. M. (1995). Iron carboxylate oxygen-centered-triangle complexes detected during electrospray use of organic acid modifiers with a comment on the Finnigan TSQ-700 electrospray inlet system. Journal of the American Society for Mass Spectrometry, 6(12), 1226-1231, doi:10.1016/1044-0305(95)00579-x.	POS	537.88	537.8790134	[M6-H6+Fe3+O]+	Triple quadrupole	Finnigan TSQ-700		ESI

    '''
    type_of_contaminant = ''
    references = []
