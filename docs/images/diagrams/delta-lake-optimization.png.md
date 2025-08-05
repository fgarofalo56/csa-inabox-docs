# PLACEHOLDER FOR DELTA LAKE OPTIMIZATION DECISION TREE

This file serves as a placeholder for the static image rendering of the Delta Lake Optimization Decision Tree diagram.

## Diagram Description

This flowchart helps users decide which Delta Lake optimization techniques to apply based on different workload characteristics with three main decision paths:

- Query Performance (Z-Ordering, Partitioning, Hybrid approach)
- Storage Optimization (VACUUM, OPTIMIZE compact, Deep Clone)
- Write Performance (Auto Optimize, Optimize write batch sizes, Low shuffle configuration)

## Original Mermaid Code

```mermaid
flowchart TD
    start[Start Optimization] --> q1{What's your<br>primary concern?}
    q1 -->|Query Performance| q2{Query Pattern?}
    q1 -->|Storage Optimization| q3{Data Size?}
    q1 -->|Write Performance| q4{Write Pattern?}
    
    q2 -->|Analytical Queries| Z_ORDER[Z-Ordering<br>Optimize for specific columns]
    q2 -->|Point Lookups| PARTITION[Partitioning<br>by lookup columns]
    q2 -->|Mixed Workload| BOTH[Z-Ordering + Partitioning<br>Hybrid approach]
    
    q3 -->|>1 TB| VACUUM[Run VACUUM<br>with retention period]
    q3 -->|>10 TB| COMPACT[Run OPTIMIZE<br>to compact small files]
    q3 -->|Any Size with<br>many deletes| DEEP_CLONE[Consider Deep Clone<br>to reclaim space]
    
    q4 -->|Many small writes| AUTO_OPTIMIZE[Enable Auto Optimize]
    q4 -->|Batch writes| OPTIMIZE_WRITES[Optimize write<br>batch sizes]
    q4 -->|Streaming| LOW_SHUFFLE[Configure for<br>low shuffle]
    
    Z_ORDER --> MONITOR[Monitor query<br>performance]
    PARTITION --> MONITOR
    BOTH --> MONITOR
    
    VACUUM --> SCHEDULE[Schedule regular<br>maintenance]
    COMPACT --> SCHEDULE
    DEEP_CLONE --> EVALUATE[Evaluate storage<br>improvements]
    
    AUTO_OPTIMIZE --> VALIDATE[Validate with<br>benchmarks]
    OPTIMIZE_WRITES --> VALIDATE
    LOW_SHUFFLE --> VALIDATE
```

## Instructions for Implementation

Replace this markdown file with an actual PNG image exported from a Mermaid rendering tool.
