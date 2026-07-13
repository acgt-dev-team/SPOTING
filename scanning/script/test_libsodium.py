
from common.windows_utils import get_imported_functions

binary = r"C:\AGCT\library-sources\libsodium-win64\bin\libsodium-26.dll"

for api in get_imported_functions(binary):
    print(api)