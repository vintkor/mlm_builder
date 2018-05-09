from facebookads.api import FacebookAdsApi
from facebookads import adobjects
from facebookads.adobjects.campaign import Campaign


class FacebookAdsApiWrapper:
    """
    Facebook Adds API wrapper
    """

    def __init__(self, my_app_id, my_app_secret, my_access_token):
        FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
        self.campaign = None

    def create_campaign(self, campaign_title, parent_id):
        self.campaign = Campaign(parent_id='act_{}'.format(parent_id))

        self.campaign.update({
            Campaign.Field.name: campaign_title,
            Campaign.Field.objective: Campaign.Objective.link_clicks,
        })

        self.campaign.remote_create(params={
            'status': Campaign.Status.paused,
        })
