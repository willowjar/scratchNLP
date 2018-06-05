
import sqlite3

from category import Variable
import featurelite
import category


def pretty_print_entry(f):
    if type(f) is str:
        return f
    elif type(f) is category.C:
        if f.semanticType() == "Object":
            if 'name' in f.keys():
                return f['name']
            elif 'definite' in f.keys():
                return "%s %s"%("the" if f['definite'] else "a", f['type'])
        elif f.semanticType() == "Place":
            location = f['location']
            article = "the" if location['definite'] else "a"
            return "%s %s %s"%(f['relation'], article, location['type'])
    elif type(f) is featurelite.Variable:
        return str(f)
    return str(f)


def extract_feature(k, event_struct):
    if k in event_struct._features:
        x = event_struct._features[k]
        try:
            return (x, pretty_print_entry(x))
        except:
            return (x, str(x))
    return (None, "NULL")


def extract_feature_dict(event_struct):
    return {'action': extract_feature('action', event_struct),
            'agent': extract_feature('agent', event_struct),
            'patient': extract_feature('patient', event_struct),
            'beneficiary': extract_feature('beneficiary', event_struct),
            'tense': extract_feature('tense', event_struct),
            'locative': extract_feature('locative', event_struct)}


class SemanticDatabase(object):
    def __init__(self):
        self.db = sqlite3.connect(":memory:")
        self.db.row_factory = sqlite3.Row
        c = self.db.cursor()
        c.execute("CREATE TABLE knowledge (action VARCHAR, agent VARCHAR, patient VARCHAR, beneficiary VARCHAR, tense VARCHAR, locative VARCHAR)")
    
    
    def add_fact(self, event_struct):
        fd = extract_feature_dict(event_struct)
        non_null_keys = [k for k, v in fd.iteritems() if v[1] != 'NULL']
        query = "INSERT INTO knowledge (%s) VALUES (%s)"%(', '.join(non_null_keys),
                                                          ', '.join(['?']*len(non_null_keys)))
        vals = tuple([fd[k][1] for k in non_null_keys])
        c = self.db.cursor()
        c.execute(query, vals)


    def print_knowledge(self):
        c = self.db.cursor()
        c.execute("SELECT * FROM knowledge")
        # Do not print duplicate entries.
        es = set()
        for row in c.fetchall():
            e = "[" + ", ".join(["%s=%s"%(k,row[k]) for k in row.keys()]) + "]"
            if e not in es:
                es.add(e)
                print e


    def yesno_query(self, event_struct):
        fd = extract_feature_dict(event_struct)
        non_null_keys = [k for k, v in fd.iteritems() if v[1] != 'NULL']
        query = "SELECT COUNT(*) FROM knowledge WHERE %s"%(" and ".join([x + "=?" for x in non_null_keys]))
        vals = tuple([fd[k][1] for k in non_null_keys])
        c = self.db.cursor()
        c.execute(query, vals)
        num_instances = c.fetchone()[0]
        return num_instances > 0


    def wh_query(self, event_struct):
        fd = extract_feature_dict(event_struct)
        non_null_keys = [k for k, v in fd.iteritems() if v[1] != 'NULL']
        wh_keys = [k for k in non_null_keys if fd[k][1].startswith('?')]
        non_wh_keys = [k for k in non_null_keys if not fd[k][1].startswith('?')]

        c = self.db.cursor()
        if len(wh_keys) == 1:
            condition = ' and '.join([k+'=?' for k in non_wh_keys])
            query = "SELECT %s FROM knowledge WHERE %s"%(wh_keys[0], condition)
            vals = tuple([fd[k][1] for k in non_wh_keys])
            c.execute(query, vals)
            return set(row[0] for row in c if row[0] is not None)
        return []
