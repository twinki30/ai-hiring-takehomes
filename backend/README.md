# Backend Developer Take-Home Task  
**Geospatial Public Infrastructure Monitoring**  

---

## Objective  
Design a REST API and geospatial database system to manage city infrastructure assets (e.g., streetlights, traffic sensors). Focus on **GIS queries**, **performance optimization**, and **scalability**. Use PostgreSQL with PostGIS and Python, with implicit challenges that encourage clever use of caching/iterators.  

---

## Note
AITL's backend is build on microservices. To simulate the same we ask you to use any Pythonic framework you want to design the APIs but keeping serverless in mind.
We recommend using fastAPI as that is the easiest but if you are aware of any other framework, that's all good!
Keep in mind that we will test you on your design pattern, code quality, AWS infrastructure understanding and general understanding of microservices. 
Timebox your work for 4 hours. Do not spend more than 4 hours on the task. You don't need to complete all sections nor should you attend all of it.
If you have any thoughts on any of these sections, do maintain them in your submission.

--- 

## Task Sections  

### 1. Basic (Mandatory)  
**Geospatial API & Database**  
- **PostgreSQL + PostGIS Setup**:  
  - Model a table with PostGIS `geometry(Point, 4326)` for coordinates. Include fields: `asset_id`, `type`, `status`, `last_maintained`.  
  - Write a script to ingest `primary_assets.json` into the DB.  
- **API Implementation**:  
  - Build a FastAPI/Flask endpoint with:  
    - `GET /assets?bbox=min_lon,min_lat,max_lon,max_lat`: Return assets within a bounding box.  
    - `GET /assets/{asset_id}`: Return details + GeoJSON point geometry.  
  - Use response validation.  
- **Code Standards**:  
  - Write tests for bounding box queries and asset creation.  
  - Enforce type hints and module-based code structure.  

---

### 2. Advanced (Optional)  
**Performance & Geospatial Complexity**  
- **High-Frequency Queries**:  
  - Implement `GET /assets/nearby?lat=...&lon=...&radius=...` to find assets within *N* meters of a point.  
  - Optimize with a GiST index on the geometry column.  
- **Hidden Challenge**:  
  - The city reports repeated API calls for the same bounding box. *Hint: Reduce redundant computation.*  
- **Batch Processing**:  
  - Write a script to update statuses from `supplement_assets.json`. Process in chunks to avoid memory overload.  

---

### 3. Exceptional (Stretch Goal)  
**Scalability & Data Integrity**  
- **Data Merging**:  
  - Deduplicate assets between datasets using:  
    - Spatial proximity (assets within 5m are duplicates).  
    - Fuzzy ID matching (e.g., "TL_001" vs "TL_01").  
  - Add `data_source` (primary/supplement) and `confidence_score` to merged records.  
- **Fault Tolerance**:  
  - Design an idempotent `POST /bulk-update` endpoint for large geospatial updates.  
- **Resource Efficiency**:  
  - Propose a way to process 100k+ asset queries without OOM errors (think **lazy evaluation**).  

---

## Submission Requirements  
1. **Code**:  
   - Python app with `geo_utils/` (spatial calculations), `api/`, `models/`.  
   - Database schema with PostGIS setup instructions.  
2. **Documentation**:  
   - `README.md`: Setup, API examples, and how to test geospatial queries.  
   - `DESIGN.md`: Explain indexing choices, caching opportunities, and AWS serverless integration ideas.  
3. **Project Plan**:  
   - Outline real-time tracking enhancements (e.g., "Use AWS Kinesis for streaming coordinates").  

---

## Evaluation Criteria  
- **GIS Skills**: Correct use of PostGIS, bounding box/radius queries.  
- **Performance**: Use of indexes, caching hints, memory-efficient batch processing.  
- **Code Quality**: Modularity, tests, and implicit use of Pythonic optimizations.  
- **Scalability**: Awareness of serverless patterns (even if not implemented).  

---

## Notes  
- **Time Management**: Focus on Basic tasks. For incomplete sections, add `DESIGN.md` notes like:  
  *"For 100k+ assets, I’d lazy-load batches via to avoid memory spikes."*  

---

---
## Submission
- Create a private repo and add AISuhasDattatreya as a reviewer to your PR. 
- Submit the PR link and the your notes (timelines, breakdown and what you've implented) to suhas@advanced-infrastructure.co.uk
- We'll go over your code together and discuss your architecture 
