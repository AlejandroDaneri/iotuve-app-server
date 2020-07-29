from business_rules import run_all
from business_rules.actions import rule_action, BaseActions
from business_rules.fields import FIELD_NUMERIC
from business_rules.variables import BaseVariables, numeric_rule_variable


class ImportanceVariables(BaseVariables):

    def __init__(self, video):
        self.video = video

    @numeric_rule_variable
    def user_posts(self):
        return self.video['user_posts']

    @numeric_rule_variable
    def user_reactions(self):
        return self.video['user_reactions']

    @numeric_rule_variable
    def user_friends(self):
        return self.video['user_friends']

    @numeric_rule_variable
    def video_days(self):
        return self.video['days']

    @numeric_rule_variable
    def video_likes(self):
        return self.video['likes']

    @numeric_rule_variable
    def video_dislikes(self):
        return self.video['dislikes']

    @numeric_rule_variable
    def video_views(self):
        return self.video['views']

    @numeric_rule_variable
    def video_comments(self):
        return self.video['comments']


class ImportanceActions(BaseActions):

    def __init__(self, video):
        self.video = video

    @rule_action(params={"importance": FIELD_NUMERIC})
    def sum_importance(self, importance):
        self.video['importance'] += importance


class ImportanceCalculator:

    def __init__(self, video):
        self.rules = []
        self.video = video

    def define_rules(self):
        self.rules += [
            {"conditions": {"any": [
                {"name": "user_posts", "operator": "greater_than_or_equal_to", "value": 0}
            ]},
             "actions": [{"name": "sum_importance", "params": {"importance": 0.75 * self.video['user_posts']}}],
            },
            {"conditions": {"any": [
                {"name": "user_reactions", "operator": "greater_than_or_equal_to", "value": 0}
            ]},
             "actions": [{"name": "sum_importance", "params": {"importance": 0.50 * self.video['user_reactions']}}],
            },
            {"conditions": {"any": [
                {"name": "user_friends", "operator": "greater_than_or_equal_to", "value": 0}
            ]},
             "actions": [{"name": "sum_importance", "params": {"importance": 0.25 * self.video['user_friends']}}],
            }
        ]

        self.rules += [
            {"conditions": {"any": [
                {"name": "video_days", "operator": "greater_than_or_equal_to", "value": 0}
            ]},
             "actions": [{"name": "sum_importance", "params": {"importance": -0.40 * self.video['days']}}],
            },
            {"conditions": {"any": [
                {"name": "video_likes", "operator": "greater_than_or_equal_to", "value": 0}
            ]},
             "actions": [{"name": "sum_importance", "params": {"importance": 0.20 * self.video['likes']}}],
            },
            {"conditions": {"any": [
                {"name": "video_dislikes", "operator": "greater_than_or_equal_to", "value": 0}
            ]},
             "actions": [{"name": "sum_importance", "params": {"importance": -0.20 * self.video['dislikes']}}],
            },
            {"conditions": {"any": [
                {"name": "video_views", "operator": "greater_than_or_equal_to", "value": 0}
            ]},
             "actions": [{"name": "sum_importance", "params": {"importance": 0.30 * self.video['views']}}],
            },
            {"conditions": {"any": [
                {"name": "video_comments", "operator": "greater_than_or_equal_to", "value": 0}
            ]},
             "actions": [{"name": "sum_importance", "params": {"importance": 0.10 * self.video['comments']}}],
            }
        ]

    def calculate_importance(self):
        self.define_rules()

        run_all(rule_list=self.rules,
                defined_variables=ImportanceVariables(self.video),
                defined_actions=ImportanceActions(self.video),
                stop_on_first_trigger=False
                )

        return self.video['importance']
