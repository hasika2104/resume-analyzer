"""Comprehensive interview preparation and coaching service."""
import json
from typing import Any

def extract_tech_stack(parsed: dict) -> dict:
    """Extract all technologies from resume."""
    return {
        "languages": parsed.get("skills", [])[:15],
        "frameworks": [s for s in parsed.get("skills", []) if any(fw in s.lower() for fw in ["react", "django", "spring", "flask", "express", "vue", "angular", "fastapi"])],
        "databases": [s for s in parsed.get("skills", []) if any(db in s.lower() for db in ["sql", "postgres", "mongo", "redis", "cassandra", "dynamodb"])],
        "tools": [s for s in parsed.get("skills", []) if any(t in s.lower() for t in ["git", "docker", "kubernetes", "aws", "gcp", "jenkins"])],
        "other": [s for s in parsed.get("skills", []) if s not in parsed.get("skills", [])[:15]],
    }


def generate_resume_based_questions(tech_stack: dict) -> dict:
    """Generate technical questions based on technologies in resume."""
    languages = tech_stack.get("languages", [])
    frameworks = tech_stack.get("frameworks", [])
    databases = tech_stack.get("databases", [])
    
    questions = {
        "beginner": [],
        "intermediate": [],
        "advanced": [],
    }
    
    # Language-specific questions
    for lang in languages[:3]:
        lang_lower = lang.lower()
        if "python" in lang_lower:
            questions["beginner"].extend([
                f"Explain list comprehensions in {lang}.",
                f"What are decorators in {lang} and how do you use them?",
                f"Explain the difference between == and 'is' in {lang}.",
            ])
            questions["intermediate"].extend([
                f"Describe async/await and concurrency patterns in {lang}.",
                f"How does garbage collection work in {lang}?",
                f"Explain metaclasses and when you would use them in {lang}.",
            ])
            questions["advanced"].extend([
                f"Explain the GIL (Global Interpreter Lock) and its implications.",
                f"How would you optimize a computationally intensive {lang} application?",
                f"Describe memory management and reference counting in {lang}.",
            ])
        elif "java" in lang_lower:
            questions["beginner"].extend([
                f"What is the difference between checked and unchecked exceptions in {lang}?",
                f"Explain inheritance, interfaces, and abstract classes in {lang}.",
                f"What is the purpose of the 'static' keyword in {lang}?",
            ])
            questions["intermediate"].extend([
                f"Explain how multithreading works in {lang}.",
                f"What are the different types of inner classes in {lang}?",
                f"Describe the Collections framework and concurrent collections.",
            ])
            questions["advanced"].extend([
                f"Explain memory model and visibility guarantees in {lang}.",
                f"How would you design a highly concurrent system in {lang}?",
                f"Describe bytecode compilation and JVM optimization techniques.",
            ])
        elif "javascript" in lang_lower or "typescript" in lang_lower:
            questions["beginner"].extend([
                f"Explain closures and scope in {lang}.",
                f"What is hoisting and how does it work?",
                f"Explain the difference between var, let, and const.",
            ])
            questions["intermediate"].extend([
                f"Describe the event loop and how asynchronous code execution works.",
                f"Explain Promises and async/await patterns.",
                f"What is prototype-based inheritance in {lang}?",
            ])
            questions["advanced"].extend([
                f"Explain the microtask and macrotask queues in the event loop.",
                f"How would you optimize {lang} performance for large-scale applications?",
                f"Describe CommonJS vs ES6 modules and tree-shaking.",
            ])
    
    # Framework-specific questions
    for framework in frameworks[:2]:
        fw_lower = framework.lower()
        if "react" in fw_lower:
            questions["beginner"].extend([
                "What is JSX and how does it work?",
                "Explain the difference between class and functional components.",
                "What are React hooks and when should you use them?",
            ])
            questions["intermediate"].extend([
                "Explain React's reconciliation algorithm (Virtual DOM).",
                "How do you manage state in a complex React application?",
                "Describe the useEffect hook and its dependency array.",
            ])
            questions["advanced"].extend([
                "How would you optimize render performance in a large React app?",
                "Explain server-side rendering (SSR) vs static generation.",
                "Describe advanced patterns like compound components and render props.",
            ])
        elif "django" in fw_lower or "flask" in fw_lower:
            questions["beginner"].extend([
                f"Explain the MVC/MVT architecture in {framework}.",
                f"How does the ORM work in {framework}?",
                f"What are middleware components in {framework}?",
            ])
            questions["intermediate"].extend([
                f"Describe authentication and authorization in {framework}.",
                f"How do you handle database migrations in {framework}?",
                f"Explain caching strategies in {framework}.",
            ])
            questions["advanced"].extend([
                f"How would you design a scalable {framework} application?",
                f"Describe background task processing with Celery.",
                f"Explain API design best practices and versioning.",
            ])
    
    # Database-specific questions
    for db in databases[:2]:
        db_lower = db.lower()
        if "sql" in db_lower or "postgres" in db_lower:
            questions["beginner"].extend([
                "Explain ACID properties in databases.",
                "What are indexes and how do they improve performance?",
                "Explain normalization and its different normal forms.",
            ])
            questions["intermediate"].extend([
                "Describe query optimization and execution plans.",
                "What are transactions and isolation levels?",
                "Explain stored procedures, triggers, and views.",
            ])
            questions["advanced"].extend([
                "How would you design a database for a high-traffic application?",
                "Describe sharding and replication strategies.",
                "Explain distributed transactions and eventual consistency.",
            ])
        elif "mongo" in db_lower:
            questions["beginner"].extend([
                "What are the differences between SQL and NoSQL databases?",
                "Explain collections, documents, and BSON in MongoDB.",
                "What are indexes in MongoDB?",
            ])
            questions["intermediate"].extend([
                "Describe aggregation pipelines in MongoDB.",
                "What are transactions in MongoDB?",
                "Explain replication sets and failover.",
            ])
            questions["advanced"].extend([
                "How would you design a scalable MongoDB schema?",
                "Describe sharding strategies and shard key selection.",
                "Explain write concerns and read preferences.",
            ])
    
    return questions


def generate_project_questions(project: dict) -> dict:
    """Generate 20 detailed interview questions for a specific project."""
    project_name = project.get("name", "Project")
    description = project.get("description", "")
    tech_used = project.get("technologies", []) if isinstance(project.get("technologies"), list) else []
    
    questions_with_answers = {
        "architecture": [
            {
                "question": f"Explain the overall architecture of {project_name}. What are the main components?",
                "answer": f"Based on the project description, {project_name} likely has frontend, backend, and database layers. Key components include the UI layer for user interaction, API layer for business logic, and data persistence layer. Additional components might include authentication, caching, and third-party integrations.",
                "difficulty": "intermediate",
            },
            {
                "question": f"What design patterns did you use in {project_name}?",
                "answer": "Common patterns include MVC/MVVM for separation of concerns, Factory pattern for object creation, Observer pattern for event handling, Singleton for shared resources, and Repository pattern for data access abstraction.",
                "difficulty": "intermediate",
            },
            {
                "question": f"How would you scale {project_name} to handle 1 million users?",
                "answer": "Scalability improvements: Load balancing across multiple server instances, database replication and read replicas, caching layer (Redis/Memcached), CDN for static assets, horizontal scaling with microservices, message queues for async processing, and monitoring/alerting systems.",
                "difficulty": "advanced",
            },
        ],
        "data_flow": [
            {
                "question": f"Walk me through the data flow when a user interacts with {project_name}.",
                "answer": "Data flow: User action → Frontend validation → API request → Backend authentication → Business logic processing → Database query → Cache check → Response serialization → Frontend rendering. Error handling and logging at each step.",
                "difficulty": "intermediate",
            },
            {
                "question": f"How do you handle data consistency in {project_name}?",
                "answer": "Data consistency strategies: Transactions for atomic operations, validation at multiple layers, optimistic/pessimistic locking, event sourcing for audit trail, eventual consistency for distributed systems, and regular backups.",
                "difficulty": "advanced",
            },
            {
                "question": f"What happens if a critical operation fails in {project_name}?",
                "answer": "Error handling: Try-catch blocks for exceptions, retry logic with exponential backoff, circuit breaker pattern, graceful degradation, detailed logging, alerts to ops team, rollback mechanisms, and fallback strategies.",
                "difficulty": "advanced",
            },
        ],
        "database": [
            {
                "question": f"Describe the database schema design for {project_name}.",
                "answer": f"Schema should include normalized tables with proper relationships, indexes on frequently queried columns, foreign keys for referential integrity, appropriate data types, and consideration for future scalability.",
                "difficulty": "intermediate",
            },
            {
                "question": f"How do you optimize database queries in {project_name}?",
                "answer": "Query optimization: Use indexes strategically, avoid N+1 queries with eager loading, write efficient joins, use query builders/ORMs, implement connection pooling, monitor slow queries, and cache frequently accessed data.",
                "difficulty": "intermediate",
            },
            {
                "question": f"How do you handle database migrations in {project_name}?",
                "answer": "Migration strategy: Version control all schema changes, test migrations in staging, use migration tools (Alembic, Flyway), have rollback plans, document changes, coordinate with teams, and automate deployment.",
                "difficulty": "beginner",
            },
        ],
        "api": [
            {
                "question": f"Describe the API design of {project_name}. What endpoints do you expose?",
                "answer": "RESTful API with standard HTTP methods (GET, POST, PUT, DELETE), consistent naming conventions, versioning strategy, proper status codes, pagination for large datasets, filtering/sorting options, and comprehensive documentation.",
                "difficulty": "intermediate",
            },
            {
                "question": f"How do you handle authentication and authorization in {project_name}?",
                "answer": "Authentication: JWT tokens, OAuth, session-based auth. Authorization: Role-based access control (RBAC), permission checking, secure token storage, token refresh strategy, logout handling, and protection against common attacks (CSRF, XSS).",
                "difficulty": "intermediate",
            },
            {
                "question": f"How do you handle rate limiting and abuse prevention in {project_name}?",
                "answer": "Rate limiting: Token bucket algorithm, sliding window counters, per-user limits, per-IP limits. Additional: CAPTCHA for suspicious activity, monitoring for anomalies, blocking malicious IPs, rate limit headers in responses.",
                "difficulty": "advanced",
            },
        ],
        "deployment": [
            {
                "question": f"Describe your deployment strategy for {project_name}.",
                "answer": "Deployment pipeline: Source control → CI/CD pipeline → automated tests → staging environment → production deployment. Tools: Docker for containerization, Kubernetes for orchestration, GitHub Actions/Jenkins for automation, monitoring with Prometheus/Grafana.",
                "difficulty": "intermediate",
            },
            {
                "question": f"How do you ensure zero downtime deployment for {project_name}?",
                "answer": "Zero downtime strategies: Blue-green deployment, canary releases, rolling updates, database migration planning, feature flags for gradual rollout, health checks, and quick rollback procedures.",
                "difficulty": "advanced",
            },
            {
                "question": f"How do you monitor {project_name} in production?",
                "answer": "Monitoring: Application performance monitoring (APM), log aggregation (ELK stack), metrics collection, distributed tracing, alerts for anomalies, dashboards, SLAs/SLOs, and incident response procedures.",
                "difficulty": "intermediate",
            },
        ],
        "challenges": [
            {
                "question": f"What was the biggest technical challenge you faced in {project_name}?",
                "answer": "Common challenges: Performance bottlenecks (optimize indexing, caching), scalability issues (horizontal scaling, microservices), complex business logic (refactoring, design patterns), integration challenges (API contracts, error handling).",
                "difficulty": "intermediate",
            },
            {
                "question": f"How would you improve {project_name} if you had more time?",
                "answer": "Improvements: Better error handling, comprehensive testing, code refactoring, performance optimization, security hardening, monitoring enhancement, documentation, user experience improvements, and feature additions.",
                "difficulty": "beginner",
            },
        ],
    }
    
    return questions_with_answers


def generate_skill_gap_analysis(parsed: dict, target_role: str = "Software Engineer") -> dict:
    """Analyze skill gaps based on resume and industry expectations."""
    current_skills = set(s.lower() for s in parsed.get("skills", []))
    
    industry_expectations = {
        "Software Engineer": {
            "essential": ["data structures", "algorithms", "git", "api design", "databases"],
            "recommended": ["system design", "microservices", "cloud platforms", "ci/cd", "testing"],
            "nice_to_have": ["devops", "ml basics", "security", "leadership"],
        },
        "Data Scientist": {
            "essential": ["python", "sql", "statistics", "machine learning", "data visualization"],
            "recommended": ["deep learning", "big data", "cloud platforms", "experiment design"],
            "nice_to_have": ["nlp", "computer vision", "model deployment", "a/b testing"],
        },
        "Frontend Developer": {
            "essential": ["javascript", "react", "html", "css", "api integration"],
            "recommended": ["typescript", "testing", "performance optimization", "accessibility"],
            "nice_to_have": ["design systems", "animation", "pwa", "ssr"],
        },
        "Backend Developer": {
            "essential": ["python/java/go", "databases", "api design", "system design", "deployment"],
            "recommended": ["microservices", "caching", "message queues", "monitoring"],
            "nice_to_have": ["devops", "blockchain", "real-time systems", "ml integration"],
        },
    }
    
    role_expectations = industry_expectations.get(target_role, industry_expectations["Software Engineer"])
    
    def check_skill_presence(skill_list):
        return [s for s in skill_list if any(skill in current_skills for skill in s.lower().split())]
    
    return {
        "target_role": target_role,
        "current_skills_count": len(current_skills),
        "essential": {
            "present": check_skill_presence(role_expectations["essential"]),
            "missing": [s for s in role_expectations["essential"] if not any(skill in current_skills for skill in s.lower().split())],
        },
        "recommended": {
            "present": check_skill_presence(role_expectations["recommended"]),
            "missing": [s for s in role_expectations["recommended"] if not any(skill in current_skills for skill in s.lower().split())],
        },
        "nice_to_have": {
            "present": check_skill_presence(role_expectations["nice_to_have"]),
            "missing": [s for s in role_expectations["nice_to_have"] if not any(skill in current_skills for skill in s.lower().split())],
        },
    }


def generate_dsa_roadmap(experience_years: float) -> dict:
    """Generate DSA (Data Structures & Algorithms) preparation roadmap."""
    difficulty = "beginner" if experience_years < 1 else ("intermediate" if experience_years < 3 else "advanced")
    
    roadmap = {
        "difficulty_level": difficulty,
        "arrays": {
            "importance": "critical",
            "topics": ["2D arrays", "sliding window", "prefix sums", "sorting"],
            "frequency": "very high",
            "expected_difficulty": "medium",
            "problems": ["Two sum", "Best time to buy/sell stock", "Container with most water", "Merge intervals"],
        },
        "strings": {
            "importance": "critical",
            "topics": ["pattern matching", "palindromes", "anagrams", "substring problems"],
            "frequency": "high",
            "expected_difficulty": "medium",
            "problems": ["Longest substring without repeating", "Valid parentheses", "Group anagrams"],
        },
        "hashing": {
            "importance": "critical",
            "topics": ["hash tables", "collision handling", "counting frequencies"],
            "frequency": "very high",
            "expected_difficulty": "easy to medium",
            "problems": ["Two sum", "Unique characters", "Frequency counter"],
        },
        "linked_lists": {
            "importance": "high",
            "topics": ["traversal", "reversal", "cycle detection", "merge"],
            "frequency": "medium",
            "expected_difficulty": "medium",
            "problems": ["Reverse linked list", "Detect cycle", "Merge sorted lists"],
        },
        "stacks_queues": {
            "importance": "high",
            "topics": ["LIFO/FIFO", "monotonic stacks", "deques"],
            "frequency": "medium",
            "expected_difficulty": "medium",
            "problems": ["Valid parentheses", "Daily temperatures", "Sliding window maximum"],
        },
        "trees": {
            "importance": "critical",
            "topics": ["traversal", "BST", "AVL trees", "segment trees"],
            "frequency": "very high",
            "expected_difficulty": "medium to hard",
            "problems": ["Inorder traversal", "Validate BST", "Binary tree level order", "LCA"],
        },
        "graphs": {
            "importance": "critical",
            "topics": ["DFS/BFS", "shortest path", "topological sort", "union-find"],
            "frequency": "high",
            "expected_difficulty": "hard",
            "problems": ["Number of islands", "Course schedule", "Alien dictionary"],
        },
        "dynamic_programming": {
            "importance": "critical",
            "topics": ["memoization", "tabulation", "DP patterns"],
            "frequency": "high",
            "expected_difficulty": "hard",
            "problems": ["Fibonacci", "Coin change", "Edit distance", "LCS"],
        },
        "recursion": {
            "importance": "high",
            "topics": ["base cases", "backtracking", "tree recursion"],
            "frequency": "medium",
            "expected_difficulty": "medium",
            "problems": ["Permutations", "Combinations", "N-queens", "Sudoku solver"],
        },
    }
    
    return roadmap


def generate_company_prep(company_type: str) -> dict:
    """Generate company-specific preparation plan."""
    prep_plans = {
        "product_companies": {
            "company_type": "Product-based Companies (Google, Meta, Amazon, etc.)",
            "focus_areas": ["System design", "DSA", "Behavioral", "Culture fit"],
            "interview_rounds": [
                {"round": "Phone Screening", "duration": "45 min", "focus": "DSA + Communication"},
                {"round": "Technical Round 1", "duration": "60 min", "focus": "DSA + Coding"},
                {"round": "Technical Round 2", "duration": "60 min", "focus": "System Design"},
                {"round": "Behavioral", "duration": "45 min", "focus": "STAR method, Leadership"},
                {"round": "Final Round", "duration": "60 min", "focus": "Culture fit + Hiring manager"},
            ],
            "tips": [
                "Master LeetCode Medium/Hard problems",
                "Understand scalability and distributed systems",
                "Practice system design questions",
                "Research company culture and products",
                "Prepare STAR stories for behavioral questions",
            ],
        },
        "service_companies": {
            "company_type": "Service-based Companies (Infosys, TCS, Wipro, etc.)",
            "focus_areas": ["Fundamentals", "Communication", "Client handling", "Team work"],
            "interview_rounds": [
                {"round": "Written Test", "duration": "90 min", "focus": "Aptitude + DSA + English"},
                {"round": "Technical Interview", "duration": "45 min", "focus": "Core concepts + Projects"},
                {"round": "HR Interview", "duration": "30 min", "focus": "Communication + Background"},
            ],
            "tips": [
                "Focus on fundamentals and core concepts",
                "Prepare project details thoroughly",
                "Work on communication skills",
                "Emphasize teamwork and adaptability",
                "Practice aptitude and logical reasoning",
            ],
        },
        "startups": {
            "company_type": "AI Startups & Emerging Tech",
            "focus_areas": ["Innovation", "Problem-solving", "Ownership", "Growth mindset"],
            "interview_rounds": [
                {"round": "Initial Chat", "duration": "30 min", "focus": "Culture + Interests"},
                {"round": "Technical Task", "duration": "take-home", "focus": "Real problem solving"},
                {"round": "Technical Discussion", "duration": "60 min", "focus": "Approach + Design"},
                {"round": "Leadership/Founder", "duration": "45 min", "focus": "Vision + Fit"},
            ],
            "tips": [
                "Show enthusiasm for the problem space",
                "Demonstrate ownership and initiative",
                "Share side projects and learning",
                "Ask thoughtful questions about product and market",
                "Emphasize ability to wear multiple hats",
            ],
        },
        "hackwithinfy": {
            "company_type": "HackWithInfy (Infosys)",
            "focus_areas": ["Hackathon skills", "Rapid development", "Innovation", "Collaboration"],
            "interview_rounds": [
                {"round": "Online Coding Test", "duration": "180 min", "focus": "2-3 DSA problems"},
                {"round": "Coding Interview", "duration": "45 min", "focus": "DSA + Live coding"},
                {"round": "Project Submission", "duration": "2-3 weeks", "focus": "Full-stack project"},
                {"round": "Project Presentation", "duration": "30 min", "focus": "Demo + Discussion"},
            ],
            "tips": [
                "Build a complete working project",
                "Focus on code quality and documentation",
                "Show project in GitHub with README",
                "Prepare impressive demo",
                "Emphasize problem-solving approach",
            ],
        },
        "placement_drive": {
            "company_type": "Campus Placement Drive",
            "focus_areas": ["DSA", "Aptitude", "Technical fundamentals", "Communication"],
            "interview_rounds": [
                {"round": "Aptitude Test", "duration": "90 min", "focus": "Quantitative + Reasoning"},
                {"round": "Technical Test", "duration": "120 min", "focus": "2-3 DSA problems"},
                {"round": "Technical Interview", "duration": "45 min", "focus": "DSA + Project"},
                {"round": "HR Interview", "duration": "30 min", "focus": "Background + Fit"},
            ],
            "tips": [
                "Master LeetCode Easy/Medium problems",
                "Practice quantitative and reasoning",
                "Know your projects in detail",
                "Prepare introduction and background",
                "Be confident and communicative",
            ],
        },
    }
    
    return prep_plans.get(company_type, prep_plans["product_companies"])


def generate_project_enhancements(project: dict) -> dict:
    """Generate enhancement suggestions for a project."""
    project_name = project.get("name", "Project")
    
    return {
        "project_name": project_name,
        "current_features": project.get("description", "").split("\n")[:3],
        "advanced_features": [
            "Real-time collaboration features (WebSockets, Operational Transformation)",
            "Advanced analytics and reporting dashboard",
            "Machine learning-based recommendations",
            "Mobile application (React Native/Flutter)",
            "Admin panel with comprehensive controls",
            "API rate limiting and advanced security",
            "Audit logging and compliance features",
            "Multi-language and localization support",
        ],
        "ai_integration_opportunities": [
            "Chatbot for user support (OpenAI API)",
            "Smart search and recommendation engine",
            "Anomaly detection and fraud prevention",
            "Sentiment analysis for user feedback",
            "Automated content moderation",
            "Predictive analytics and forecasting",
            "Natural language processing for queries",
        ],
        "cloud_deployment": [
            "AWS: ECS on EC2, RDS for database, S3 for storage, CloudFront for CDN",
            "Google Cloud: App Engine for backend, Cloud SQL for database, Cloud Storage",
            "Azure: App Service for backend, Azure SQL Database, Blob Storage",
            "Recommended: Use managed services for easier scaling",
            "Implement auto-scaling based on load",
            "Use CDN for static assets",
            "Implement disaster recovery and backup",
        ],
        "production_improvements": [
            "Comprehensive error handling and logging",
            "Database query optimization and indexing",
            "Caching strategy (Redis for session/data caching)",
            "Load testing and performance benchmarking",
            "Security audit and penetration testing",
            "API documentation (Swagger/OpenAPI)",
            "Unit and integration tests (>80% coverage)",
            "CI/CD pipeline automation",
        ],
        "monetization_strategies": [
            "Freemium model (basic features free, premium paid)",
            "Subscription tiers based on features/usage",
            "One-time purchase or lifetime license",
            "API usage-based pricing",
            "White-label solution for enterprises",
            "Affiliate or referral program",
            "Premium support plans",
        ],
        "interviewer_impressive_features": [
            "Implement scalability from day one (horizontal scaling)",
            "Production-ready code with proper error handling",
            "Comprehensive documentation and clean code",
            "Security best practices (encryption, authentication, validation)",
            "Performance optimization (caching, indexing, async operations)",
            "Monitoring and alerting system in place",
            "Open-source contributions or GitHub presence",
            "Thought leadership through blog posts or talks",
        ],
    }


def generate_preparation_plan(days: int, difficulty: str) -> dict:
    """Generate a structured preparation plan for given number of days."""
    weeks = days // 7
    
    plan = {
        "duration_days": days,
        "weeks": weeks,
        "difficulty_level": difficulty,
        "weekly_schedule": [],
    }
    
    if difficulty == "beginner":
        topics_per_week = [
            {"week": 1, "topics": ["Basics of Data Structures", "Arrays", "Strings"], "hours": 20, "target_problems": 10},
            {"week": 2, "topics": ["Hashing", "Linked Lists"], "hours": 20, "target_problems": 10},
            {"week": 3, "topics": ["Stacks", "Queues"], "hours": 15, "target_problems": 8},
            {"week": 4, "topics": ["Basic Trees", "BFS/DFS"], "hours": 20, "target_problems": 10},
            {"week": 5, "topics": ["Graphs", "Topological Sort"], "hours": 20, "target_problems": 10},
            {"week": 6, "topics": ["Dynamic Programming Basics"], "hours": 20, "target_problems": 8},
            {"week": 7, "topics": ["Interview Questions", "Mock Interviews"], "hours": 15, "target_problems": 5},
            {"week": 8, "topics": ["System Design Basics", "Review"], "hours": 15, "target_problems": 3},
        ]
    elif difficulty == "intermediate":
        topics_per_week = [
            {"week": 1, "topics": ["Advanced Arrays", "Sliding Window"], "hours": 18, "target_problems": 12},
            {"week": 2, "topics": ["Advanced Trees", "Segment Trees"], "hours": 18, "target_problems": 12},
            {"week": 3, "topics": ["Advanced Graphs", "Shortest Path Algorithms"], "hours": 18, "target_problems": 12},
            {"week": 4, "topics": ["Dynamic Programming Advanced"], "hours": 20, "target_problems": 10},
            {"week": 5, "topics": ["System Design Concepts"], "hours": 15, "target_problems": 5},
            {"week": 6, "topics": ["Behavioral Preparation", "Mock Interviews"], "hours": 12, "target_problems": 3},
            {"week": 7, "topics": ["Company-specific Preparation"], "hours": 12, "target_problems": 2},
            {"week": 8, "topics": ["Final Review", "Weak Areas"], "hours": 15, "target_problems": 5},
        ]
    else:  # advanced
        topics_per_week = [
            {"week": 1, "topics": ["Complex System Design"], "hours": 18, "target_problems": 3},
            {"week": 2, "topics": ["Distributed Systems", "Scalability"], "hours": 18, "target_problems": 3},
            {"week": 3, "topics": ["Advanced DSA + Hard Problems"], "hours": 20, "target_problems": 8},
            {"week": 4, "topics": ["Microservices Architecture"], "hours": 15, "target_problems": 2},
            {"week": 5, "topics": ["Database Design at Scale"], "hours": 15, "target_problems": 2},
            {"week": 6, "topics": ["Mock Interviews with Experts"], "hours": 12, "target_problems": 2},
            {"week": 7, "topics": ["Leadership & Technical Vision"], "hours": 10, "target_problems": 1},
            {"week": 8, "topics": ["Final Preparation", "Weak Areas Review"], "hours": 10, "target_problems": 2},
        ]
    
    plan["weekly_schedule"] = topics_per_week[:weeks] if weeks < len(topics_per_week) else topics_per_week
    
    return plan


def calculate_interview_readiness_score(parsed: dict, experience_years: float) -> dict:
    """Calculate a comprehensive interview readiness score."""
    skills = set(s.lower() for s in parsed.get("skills", []))
    experience = parsed.get("experience", [])
    projects = parsed.get("projects", [])
    education = parsed.get("education", [])
    
    score_breakdown = {}
    
    # DSA Knowledge (20 points)
    dsa_score = 0
    dsa_topics = ["arrays", "strings", "hashing", "linked", "stack", "queue", "tree", "graph", "dynamic"]
    for topic in dsa_topics:
        if any(topic in s for s in skills):
            dsa_score += 2
    score_breakdown["dsa_knowledge"] = min(20, dsa_score)
    
    # Technical Skills (20 points)
    tech_score = 0
    if any(lang in skills for lang in ["python", "java", "javascript", "golang", "rust", "cpp"]):
        tech_score += 5
    if any(fw in skills for fw in ["django", "spring", "react", "fastapi", "nodejs"]):
        tech_score += 5
    if any(db in skills for db in ["sql", "postgres", "mongodb", "redis"]):
        tech_score += 5
    if any(tool in skills for tool in ["git", "docker", "kubernetes", "aws", "gcp"]):
        tech_score += 5
    score_breakdown["technical_skills"] = tech_score
    
    # Project Experience (20 points)
    project_score = len(projects) * 4
    for project in projects:
        if project.get("description"):
            project_score += 2
    score_breakdown["projects"] = min(20, project_score)
    
    # Work Experience (20 points)
    exp_score = min(20, experience_years * 4)
    score_breakdown["work_experience"] = exp_score
    
    # System Design Knowledge (10 points)
    sd_score = 0
    if experience_years >= 3:
        sd_score += 5
    if any(tech in skills for tech in ["microservice", "scalability", "distributed", "cache"]):
        sd_score += 5
    score_breakdown["system_design"] = sd_score
    
    # Soft Skills & Communication (10 points)
    # Based on project quality and job descriptions
    soft_score = 5
    if len(experience) >= 2:
        soft_score += 5
    score_breakdown["soft_skills"] = soft_score
    
    total_score = sum(score_breakdown.values())
    readiness_level = "Expert" if total_score >= 90 else ("Advanced" if total_score >= 75 else ("Intermediate" if total_score >= 60 else "Beginner"))
    
    return {
        "total_score": total_score,
        "max_score": 100,
        "percentage": (total_score / 100) * 100,
        "readiness_level": readiness_level,
        "breakdown": score_breakdown,
        "strengths": [k for k, v in score_breakdown.items() if v >= 15],
        "areas_to_improve": [k for k, v in score_breakdown.items() if v < 10],
    }


def generate_complete_interview_roadmap(parsed: dict, experience_years: float) -> dict:
    """Generate complete interview coaching roadmap."""
    tech_stack = extract_tech_stack(parsed)
    target_role = "Software Engineer"  # Can be enhanced with role detection
    
    return {
        "resume_analysis": {
            "tech_stack": tech_stack,
            "total_skills": len(parsed.get("skills", [])),
            "projects_count": len(parsed.get("projects", [])),
            "experience_years": experience_years,
        },
        "technical_questions": generate_resume_based_questions(tech_stack),
        "skill_gap_analysis": generate_skill_gap_analysis(parsed, target_role),
        "dsa_roadmap": generate_dsa_roadmap(experience_years),
        "interview_readiness_score": calculate_interview_readiness_score(parsed, experience_years),
        "projects_analysis": [
            {
                "project": p.get("name", "Project"),
                "questions": generate_project_questions(p),
                "enhancements": generate_project_enhancements(p),
            }
            for p in parsed.get("projects", [])[:3]
        ],
    }
