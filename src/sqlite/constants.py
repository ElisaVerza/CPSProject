from os.path import dirname, realpath

RESOURCE_FOLD = dirname(realpath(__file__))
DB_NAME = RESOURCE_FOLD + "/cache.db"
CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS topics (topic_id INTEGER PRIMARY KEY, topic_value VARCHAR, topic_source_note VARCHAR);
CREATE TABLE IF NOT EXISTS indicators (indicator_id INTEGER PRIMARY KEY);
CREATE TABLE IF NOT EXISTS observables (observable_id INTEGER PRIMARY KEY);
"""
INSERT_ALL_TOPICS = "INSERT OR IGNORE INTO topics(topic_id, topic_value, topic_source_note) VALUES (?, ?, ?)"
GET_TOPIC = "SELECT * FROM topics WHERE topic_id =:topic_id"
REMOVE_TOPIC = "DELETE FROM topics WHERE topic_id =:topic_id"
