from py2neo import Graph, Node, Relationship
from django.core.management import BaseCommand
from django.conf import settings
import json


class Command(BaseCommand):
    help = 'imports impression data'

    def handle(self, *args, **kwargs):
        graph = Graph(settings.GRAPH_URL)
        # dropping uniqueness contraints
        graph.schema.drop_uniqueness_constraint('Company', 'id')
        graph.schema.drop_uniqueness_constraint('User', 'id')
        graph.schema.drop_uniqueness_constraint('User', 'email')
        graph.schema.create_uniqueness_constraint('Visitor', 'key')
        graph.schema.drop_uniqueness_constraint('Campaign', 'id')
        graph.schema.drop_uniqueness_constraint('Impression', 'id')
        graph.schema.drop_uniqueness_constraint('Postal', 'code')
        graph.schema.drop_uniqueness_constraint('City', 'name')
        graph.schema.drop_uniqueness_constraint('Country', 'name')
        # create initial labels
        graph.schema.create_uniqueness_constraint('Company', 'id')
        graph.schema.create_uniqueness_constraint('User', 'id')
        graph.schema.create_uniqueness_constraint('User', 'email')
        graph.schema.create_uniqueness_constraint('Visitor', 'key')
        graph.schema.create_uniqueness_constraint('Campaign', 'id')
        graph.schema.create_uniqueness_constraint('Impression', 'id')
        graph.schema.create_uniqueness_constraint('Postal', 'code')
        graph.schema.create_uniqueness_constraint('City', 'name')
        graph.schema.create_uniqueness_constraint('Country', 'name')
        # importing models
        from apps.users.models import User, Visitor
        from apps.companies.models import Company
        from apps.campaigns.models import Campaign
        from apps.impressions.models import Impression
        # importing serializers
        from apps.companies.api.serializers import BaseCompanySerializer
        from apps.campaigns.api.serializers import BaseCampaignSerializer
        from apps.impressions.api.serializers import ImpressionSerializer
        from apps.dashboard.serializers import DashboardUserSerializer
        for company in Company.objects.all():
            # ncompany = Node.cast('Company', CompanySerializer(company).data)
            print 'company: %s' %(company.id)
            ncompany = graph.merge_one('Company', 'id', company.id)
            print BaseCompanySerializer(company).data
            ncompany.properties.update(BaseCompanySerializer(company).data)
            graph.push(ncompany)
            for user in company.users.all():
                nuser = graph.merge_one('User', 'email', user.email)
                nuser.properties.update(DashboardUserSerializer(user).data)
                graph.push(nuser)
                rel = Relationship.cast(ncompany, 'CompanyUser', nuser)
                graph.create_unique(rel)
            for campaign in  company.campaigns.all():
                print 'campaign: %s' %(campaign.id)
                ncampaign = graph.merge_one('Campaign', 'id', campaign.id)
                ncampaign.properties.update(BaseCampaignSerializer(campaign).data)
                graph.push(ncampaign)
                rel = Relationship.cast(ncompany, 'CompanyCampaign', ncampaign)
                graph.create_unique(rel)
                for impression in campaign.impressions.all():
                    meta = impression.hydrate_meta
                    visitor = graph.merge_one('Visitor', 'key', meta['visitor'])
                    if meta['country']:
                        country = graph.merge_one('Country', 'name', meta['country'])
                        graph.create_unique(
                            Relationship.cast(visitor, 'CampaignVisitorCountry', country))
                        graph.create_unique(
                            Relationship.cast(visitor, 'CampaignVisitor', ncampaign))
                        graph.create_unique(
                            Relationship.cast(country, 'CampaignCountry', ncampaign))
                        if meta['city']:
                            city = graph.merge_one('City', 'name', meta['city'])
                            graph.create_unique(
                                    Relationship.cast(city, 'CampaignCity', ncampaign)
                                )
                            graph.create_unique(
                                Relationship.cast(visitor, 'VistitorCity', city))
                            graph.create_unique(
                                Relationship.cast(city, 'CityCountry', country))
                            if meta['postal_code']:
                                postal = graph.merge_one('Postal', 'code', meta['postal_code'])
                                graph.create_unique(
                                    Relationship.cast(postal, 'CityPostalCode', city))
                                graph.create_unique(
                                    Relationship.cast(postal, 'CampaignPostalCode', ncampaign))
                                graph.create_unique(
                                    Relationship.cast(visitor, 'VistorPostalCode', postal))
        # for campaign in Campaign.objects.all():
        #     campaign = CampaignSerializer(campaign).data
        #     campaign = Node.cast('Campaign', campaign)
        #     graph.create(campaign)
        # for impression in Impression.objects.all():
        #     impression.hydrate_meta()
        #     meta = impression.meta
        #     #meta['impression'] = impression.id
        #     meta = Node.cast('ImpressionMeta', meta)
        #     graph.create(meta)
        #     impression = ImpressionSerializer(impression).data
        #     impression = Node.cast('Impression', impression)
        #     graph.create(impression)
        # for iu in ImpressionUser.objects.all():
        #     iu = ImpressionUserSerializer(iu).data
        #     iu = Node.cast('ImpressionUser', iu)
        #     graph.create(iu)
        # for user in User.objects.all():
        #     user = DashboardUserSerializer(user).data
        #     user = Node.cast('User', user)
        #     graph.create(user)





