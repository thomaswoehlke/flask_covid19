from flask_covid19.data_all.all_service_download_mixins import AllServiceMixinDownload
from flask_covid19.data_all.all_service_import_mixins import AllServiceMixinImport
from flask_covid19.data_all.all_service_update_full_mixins import (
    AllServiceMixinUpdateFull,
)
from flask_covid19.data_all.all_service_update_mixins import AllServiceMixinUpdate


class AllServiceMixin(
    AllServiceMixinUpdateFull,
    AllServiceMixinUpdate,
    AllServiceMixinDownload,
    AllServiceMixinImport,
):
    pass
