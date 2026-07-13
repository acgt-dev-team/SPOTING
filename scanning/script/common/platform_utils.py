from common.os_utils import OS_TYPE

if OS_TYPE == "windows":
    from common.windows_utils import *
else:
    from common.linux_utils import *