from os.path import dirname, realpath

RESOURCE_FOLD = dirname(realpath(__file__))
DB_NAME = RESOURCE_FOLD + "/cache.db"

# QUERY DI CREAZIONE TABELLE
CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS topics (topic_id INTEGER PRIMARY KEY, topic_value VARCHAR, topic_source_note VARCHAR);
CREATE TABLE IF NOT EXISTS indicators (indicator_id VARCHAR PRIMARY KEY, indicator_name VARCHAR, sourceNote VARCHAR);
CREATE TABLE IF NOT EXISTS indicator_topics (
    indicator_id VARCHAR NOT NULL, 
    topic_id INTEGER NOT NULL, 
    FOREIGN KEY (indicator_id) REFERENCES indicators(indicator_id) 
        ON DELETE CASCADE ON UPDATE NO ACTION, 
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id) 
        ON DELETE CASCADE ON UPDATE NO ACTION, 
    PRIMARY KEY(indicator_id, topic_id));
CREATE TABLE IF NOT EXISTS observables (observable_id INTEGER PRIMARY KEY, country VARCHAR, date VARCHAR, value FLOAT);
"""
# QUERY PER TOPICS
# Se i dati sono già presenti, li aggiorna, altrimenti li inserisce
INSERT_ALL_TOPICS = "REPLACE INTO topics(topic_id, topic_value, topic_source_note) VALUES (?, ?, ?)"
GET_TOPIC = "SELECT * FROM topics WHERE topic_id =:topic_id"
GET_ALL_TOPICS = "SELECT * FROM topics"
UPDATE_TOPIC = "UPDATE topics SET topic_value = ?, topic_source_note = ? WHERE topic_id = ? "
REMOVE_TOPIC = "DELETE FROM topics WHERE topic_id =:topic_id"

# QUERY PER INDICATORS
INSERT_INDICATORS = "REPLACE INTO indicators(indicator_id, indicator_name, sourceNote) VALUES (?,?,?)"
INSERT_INDICATOR_TOPICS = "REPLACE INTO indicator_topics(indicator_id, topic_id) VALUES (?,?)"
GET_INDICATOR = "SELECT * FROM indicators i WHERE i.indicator_id = :indicator_id"
GET_INDICATOR_TOPICS = "SELECT it.topic_id FROM indicator_topics it WHERE it.indicator_id = :indicator_id"
GET_INDICATORS_FROM_TOPIC_ID = "SELECT it.indicator_id FROM indicator_topics it WHERE it.topic_id = :topic_id"
UPDATE_INDICATOR = "UPDATE indicators SET indicator_name = ?, sourceNote = ? WHERE indicator_id= ?"
REMOVE_INDICATOR = "DELETE FROM indicators WHERE indicator_id = :indicator_id"
REMOVE_INDICATOR_TOPICS = "DELETE FROM indicator_topics WHERE indicator_id = :indicator_id"
