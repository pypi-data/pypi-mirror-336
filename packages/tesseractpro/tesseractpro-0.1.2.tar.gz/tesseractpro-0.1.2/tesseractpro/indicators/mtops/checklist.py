from ...tools import TurningPoint


class Checklist:
    def __init__(self, tpro):
        self.tpro = tpro

    def get_scores(self, turningpoint: TurningPoint) -> str:
        data = self.tpro.rest.get(
            f"indicator/mtops/score/{turningpoint.get_id()}")
        return data['enabled']

    def get_list(self):
        data = self.tpro.rest.get("indicator/mtops/list")
        return data
