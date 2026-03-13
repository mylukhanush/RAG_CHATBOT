import sqlite3
import json
import hashlib

class CacheManager:
    def __init__(self, db_path="cache.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initializes the SQLite database and creates the cache table."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS query_cache (
                query_hash TEXT PRIMARY KEY,
                query_text TEXT,
                answer TEXT,
                sources TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def _hash_query(self, query):
        """Creates a SHA-256 hash of the query for efficient lookup."""
        return hashlib.sha256(query.strip().lower().encode()).hexdigest()

    def get_cached_response(self, query):
        """
        Retrieves a cached response for the given query.
        Returns (answer, sources) if found, otherwise (None, None).
        """
        query_hash = self._hash_query(query)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT answer, sources FROM query_cache WHERE query_hash = ?', (query_hash,))
        result = cursor.fetchone()
        conn.close()

        if result:
            answer, sources_json = result
            sources = json.loads(sources_json)
            return answer, sources
        return None, None

    def cache_response(self, query, answer, sources):
        """
        Stores a query and its response in the cache.
        'sources' is expected to be a list of Document objects or similar, 
        which will be converted to a list of strings for storage.
        """
        query_hash = self._hash_query(query)
        # Convert sources to a list of page_content if they are Document objects
        if sources and hasattr(sources[0], 'page_content'):
            sources_to_store = [doc.page_content for doc in sources]
        else:
            sources_to_store = sources

        sources_json = json.dumps(sources_to_store)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO query_cache (query_hash, query_text, answer, sources)
            VALUES (?, ?, ?, ?)
        ''', (query_hash, query, answer, sources_json))
        conn.commit()
        conn.close()

    def clear_cache(self):
        """Clears all entries from the cache."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM query_cache')
        conn.commit()
        conn.close()
