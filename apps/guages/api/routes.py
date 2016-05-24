from rest_framework.routers import SimpleRouter

from .viewsets import AssetViewSet, AssetReportViewSet

router = SimpleRouter()
router.register('assets', AssetViewSet, base_name='assets')
router.register('asset-reporter', AssetReportViewSet, base_name='asset-reporter')
