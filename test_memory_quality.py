"""Test memory quality tools"""
from carma_core.memory_quality import MemoryDeduplicator

print("Testing Memory Deduplication...\n")
d = MemoryDeduplicator()
r = d.deduplicate(dry_run=True)

print(f"\nResults:")
print(f"  Total fragments: {r['total_fragments']}")
print(f"  Duplicate groups: {r['duplicate_groups']}")
print(f"  Total duplicates: {r['total_duplicates']}")
print(f"  Recommended removals: {r['recommended_removals']}")
print(f"  Dry run: {r['dry_run']}")

if r['recommended_removals'] > 0:
    print(f"\nTop 5 removals: {r['removals'][:5]}")

