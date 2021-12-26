from data_all.framework.services.all_service_download_mixins import AllServiceMixinDownload
from data_all.framework.services.all_service_import_mixins import AllServiceMixinImport
from data_all.framework.services.all_service_update_full_mixins import (
    AllServiceMixinUpdateFull,
)
from data_all.framework.services.all_service_update_mixins import AllServiceMixinUpdate


class AllServiceMixin(
    AllServiceMixinUpdateFull,
    AllServiceMixinUpdate,
    AllServiceMixinDownload,
    AllServiceMixinImport,
):
    pass
