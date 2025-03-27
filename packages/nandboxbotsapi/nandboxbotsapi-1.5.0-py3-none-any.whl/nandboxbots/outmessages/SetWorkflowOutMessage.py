import json

from nandboxbots.outmessages.OutMessage import OutMessage


class SetWorkflowOutMessage(OutMessage):
    __KEY_USER_ID = "user_id"
    __KEY_SCREEN_ID = "screen_id"
    __KEY_WORKFLOW_CELL = "workflow_cell"
    __KEY_APP_ID = "app_id"
    __KEY_DISABLE_NOTIFICATION = "disable_notification"

    userId = None
    appId = None
    screenId = None
    disableNotification = None
    workflowCell = []

    def __init__(self):
        self.method = "setWorkflow"

    def to_json_obj(self):
        _, dictionary = super(SetWorkflowOutMessage, self).to_json_obj()

        if self.workflowCell is not None:
            dictionary[self.__KEY_WORKFLOW_CELL] = self.workflowCell
        if self.userId is not None:
            dictionary[self.__KEY_USER_ID] = self.userId
        if self.appId is not None:
            dictionary[self.__KEY_APP_ID] = self.appId
        if self.screenId is not None:
            dictionary[self.__KEY_SCREEN_ID] = self.screenId
        if self.disableNotification is not None:
            dictionary[self.__KEY_DISABLE_NOTIFICATION] = self.disableNotification

        return json.dumps(dictionary), dictionary
