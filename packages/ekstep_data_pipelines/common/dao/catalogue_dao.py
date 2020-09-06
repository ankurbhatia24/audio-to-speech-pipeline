import json


class CatalogueDao:

    def __init__(self, postgres_client):
        self.postgres_client = postgres_client

    def get_utterances(self, audio_id):
        print('postgres_client \
            .execute_query signature:' + str(self.postgres_client.execute_query))
        parm_dict = {'audio_id': audio_id}
        utterances = self.postgres_client \
            .execute_query('select utterances_files_list from media_metadata_staging where audio_id = :audio_id'
                           , **parm_dict)
        return utterances

    def update_utterances(self, audio_id, utterances):
        update_query = 'update media_metadata_staging ' \
                       'set utterances_files_list = :utterances where audio_id = :audio_id'
        parm_dict = {'utterances': utterances, 'audio_id': audio_id}
        self.postgres_client.execute_update(update_query, **parm_dict)
        return True

    def find_utterance_by_name(self, utterances, name):
        json_dict = json.loads(utterances)
        filtered_utterances = list(filter(lambda d: d['name'] == name, json_dict))
        if len(filtered_utterances) > 0:
            return filtered_utterances[0]
        else:
            return None