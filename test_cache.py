from cache_manager import CacheManager
import os

def test_cache():
    db_path = "test_cache.db"
    # Ensure fresh start
    if os.path.exists(db_path):
        os.remove(db_path)
    
    cache = CacheManager(db_path=db_path)
    
    query = "What is the capital of France?"
    answer = "The capital of France is Paris."
    sources = ["Source: Geography Book", "Source: Wikipedia"]
    
    print(f"Testing caching for query: '{query}'")
    
    # Test 1: Cache hit (should be None initially)
    cached_ans, cached_srcs = cache.get_cached_response(query)
    assert cached_ans is None, "Cache should be empty initially"
    print("✓ Cache is empty initially as expected.")
    
    # Test 2: Store and Retrieve
    cache.cache_response(query, answer, sources)
    cached_ans, cached_srcs = cache.get_cached_response(query)
    
    assert cached_ans == answer, f"Expected {answer}, got {cached_ans}"
    assert cached_srcs == sources, f"Expected {sources}, got {cached_srcs}"
    print("✓ Successfully stored and retrieved from cache.")
    
    # Test 3: Clear Cache
    cache.clear_cache()
    cached_ans, cached_srcs = cache.get_cached_response(query)
    assert cached_ans is None, "Cache should be empty after clear_cache()"
    print("✓ Successfully cleared cache.")
    
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)
    print("\nAll tests passed!")

if __name__ == "__main__":
    test_cache()
