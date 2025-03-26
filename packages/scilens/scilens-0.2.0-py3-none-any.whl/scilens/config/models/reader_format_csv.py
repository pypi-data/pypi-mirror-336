_A=None
from pydantic import BaseModel,Field
from scilens.config.models.reader_format_cols_curve import ReaderColsCurveParserConfig
class ReaderCsvConfig(BaseModel):ignore_columns:list[str]|_A=Field(default=_A,description='Liste des noms des colonnes à ignorer. (Valide seulement si la première ligne est les en-têtes)');delimiter:str|_A=Field(default=',',description='Délimiteur de colonnes.');quotechar:str|_A=Field(default='"',description='Délimiteur de texte.');curve_parser:ReaderColsCurveParserConfig|_A=Field(default=_A,description='Parseur de courbe à utiliser.')