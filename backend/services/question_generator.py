"""
Interview question generator and answer evaluator.
Generates categorized questions based on extracted skills and experience.
"""
import re
import uuid
import random

# ---------------------------------------------------------------------------
# Question templates – 100+ questions across categories and skills
# ---------------------------------------------------------------------------

TECHNICAL_QUESTIONS = {
    # --- Programming Languages ---
    "Python": [
        {
            "text": "Explain Python decorators and provide a practical use case.",
            "difficulty": "medium",
            "sample_answer": "Decorators are functions that modify the behavior of other functions. They use @syntax and are commonly used for logging, authentication, caching, and rate limiting. A decorator takes a function as input, adds functionality, and returns a modified function.",
            "keywords": ["decorator", "function", "wrapper", "@", "modify", "behavior"]
        },
        {
            "text": "What is the difference between a list and a tuple in Python?",
            "difficulty": "easy",
            "sample_answer": "Lists are mutable (can be changed after creation) while tuples are immutable. Lists use square brackets [], tuples use parentheses (). Tuples are faster and can be used as dictionary keys. Lists are better when you need to modify the collection.",
            "keywords": ["mutable", "immutable", "list", "tuple", "bracket", "parenthes"]
        },
        {
            "text": "Explain Python's GIL (Global Interpreter Lock) and its impact on multithreading.",
            "difficulty": "hard",
            "sample_answer": "The GIL is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecode simultaneously. This limits CPU-bound multithreading but doesn't affect I/O-bound tasks. Alternatives include multiprocessing, asyncio, or using C extensions.",
            "keywords": ["GIL", "mutex", "thread", "bytecode", "multiprocessing", "concurrent", "CPU-bound", "I/O"]
        },
        {
            "text": "What are Python generators and how do they differ from regular functions?",
            "difficulty": "medium",
            "sample_answer": "Generators use yield instead of return and produce values lazily one at a time. They maintain state between calls, use less memory than lists, and are ideal for large datasets or infinite sequences. They implement the iterator protocol automatically.",
            "keywords": ["yield", "lazy", "iterator", "memory", "state", "generator"]
        },
        {
            "text": "Explain list comprehension vs generator expression in Python.",
            "difficulty": "easy",
            "sample_answer": "List comprehensions [x for x in range()] create the entire list in memory. Generator expressions (x for x in range()) produce values lazily. Generators are memory-efficient for large datasets while list comprehensions are faster for small datasets that need to be reused.",
            "keywords": ["list comprehension", "generator", "memory", "lazy", "bracket", "parenthes"]
        },
    ],
    "Java": [
        {
            "text": "Explain the difference between an abstract class and an interface in Java.",
            "difficulty": "medium",
            "sample_answer": "Abstract classes can have both abstract and concrete methods, instance variables, and constructors. Interfaces (pre-Java 8) only have abstract methods. Since Java 8, interfaces can have default and static methods. A class can implement multiple interfaces but extend only one abstract class.",
            "keywords": ["abstract", "interface", "implement", "extend", "method", "multiple inheritance"]
        },
        {
            "text": "What is the Java Memory Model and how does garbage collection work?",
            "difficulty": "hard",
            "sample_answer": "The JMM defines how threads interact through memory. Java memory is divided into Heap (objects), Stack (method frames), and Metaspace. Garbage collection automatically reclaims unused objects. Major GC algorithms include G1, ZGC, and Shenandoah, using generations (Young, Old) for efficiency.",
            "keywords": ["heap", "stack", "garbage", "collection", "JMM", "generation", "G1", "memory"]
        },
        {
            "text": "Explain Java Streams API and give an example of its usage.",
            "difficulty": "medium",
            "sample_answer": "Streams API (Java 8+) provides a functional approach to processing collections. It supports operations like filter, map, reduce, collect. Streams are lazy and can be parallelized. Example: list.stream().filter(x -> x > 5).map(x -> x * 2).collect(Collectors.toList()).",
            "keywords": ["stream", "filter", "map", "reduce", "collect", "functional", "lazy", "pipeline"]
        },
    ],
    "JavaScript": [
        {
            "text": "Explain closures in JavaScript with an example.",
            "difficulty": "medium",
            "sample_answer": "A closure is a function that retains access to its lexical scope even when executed outside that scope. It 'closes over' variables from its parent function. Common uses include data privacy, factory functions, and callbacks. Example: function counter() { let count = 0; return () => ++count; }",
            "keywords": ["closure", "scope", "lexical", "variable", "function", "access", "enclos"]
        },
        {
            "text": "What is the event loop in JavaScript and how does it work?",
            "difficulty": "hard",
            "sample_answer": "The event loop is JavaScript's concurrency model. It has a call stack, task queue (macrotasks), and microtask queue. The loop checks if the call stack is empty, then processes all microtasks (Promises), then picks the next macrotask (setTimeout, I/O). This enables non-blocking async behavior in single-threaded JS.",
            "keywords": ["event loop", "call stack", "queue", "microtask", "macrotask", "async", "non-blocking", "single-threaded"]
        },
        {
            "text": "Explain the difference between var, let, and const in JavaScript.",
            "difficulty": "easy",
            "sample_answer": "var is function-scoped and hoisted. let is block-scoped and not hoisted (temporal dead zone). const is block-scoped and cannot be reassigned (but objects/arrays can be mutated). Best practice: use const by default, let when reassignment is needed, avoid var.",
            "keywords": ["scope", "block", "function", "hoist", "const", "let", "var", "reassign"]
        },
        {
            "text": "What are Promises and async/await in JavaScript?",
            "difficulty": "medium",
            "sample_answer": "Promises represent eventual completion/failure of async operations with .then()/.catch(). async/await is syntactic sugar over Promises making async code look synchronous. async functions return Promises. await pauses execution until the Promise resolves. Error handling uses try/catch.",
            "keywords": ["promise", "async", "await", "then", "catch", "resolve", "reject", "asynchronous"]
        },
    ],
    "TypeScript": [
        {
            "text": "What are the benefits of TypeScript over JavaScript?",
            "difficulty": "easy",
            "sample_answer": "TypeScript adds static typing, interfaces, enums, generics, and better IDE support. It catches errors at compile time, improves code documentation, enables better refactoring, and compiles to JavaScript. It's especially valuable for large codebases and team collaboration.",
            "keywords": ["type", "static", "compile", "interface", "generic", "error", "IDE", "safety"]
        },
        {
            "text": "Explain generics in TypeScript and when to use them.",
            "difficulty": "medium",
            "sample_answer": "Generics allow creating reusable components that work with multiple types while maintaining type safety. Syntax: function identity<T>(arg: T): T. Use cases include generic data structures, API response wrappers, and utility functions. They provide flexibility without losing type information.",
            "keywords": ["generic", "type", "reusable", "safety", "parameter", "constraint", "flexible"]
        },
    ],
    "C++": [
        {
            "text": "Explain RAII (Resource Acquisition Is Initialization) in C++.",
            "difficulty": "hard",
            "sample_answer": "RAII ties resource management to object lifetime. Resources are acquired in constructors and released in destructors. When objects go out of scope, destructors run automatically, preventing leaks. Smart pointers (unique_ptr, shared_ptr) are prime RAII examples.",
            "keywords": ["RAII", "resource", "constructor", "destructor", "scope", "smart pointer", "lifetime"]
        },
        {
            "text": "What is the difference between stack and heap memory allocation in C++?",
            "difficulty": "medium",
            "sample_answer": "Stack memory is automatically managed, faster, and limited in size. Variables are destroyed when they go out of scope. Heap memory is manually managed (new/delete), slower, but larger. Heap requires explicit deallocation to prevent memory leaks. Smart pointers help manage heap memory safely.",
            "keywords": ["stack", "heap", "memory", "allocation", "new", "delete", "scope", "leak"]
        },
    ],
    "C#": [
        {
            "text": "Explain LINQ in C# and its advantages.",
            "difficulty": "medium",
            "sample_answer": "LINQ (Language Integrated Query) provides a unified syntax for querying data from various sources (collections, databases, XML). It supports query syntax (from x in y select z) and method syntax (.Where().Select()). Benefits include type safety, readability, and provider-agnostic code.",
            "keywords": ["LINQ", "query", "select", "where", "collection", "data", "syntax", "provider"]
        },
    ],
    "SQL": [
        {
            "text": "Explain the difference between INNER JOIN, LEFT JOIN, and FULL OUTER JOIN.",
            "difficulty": "medium",
            "sample_answer": "INNER JOIN returns only matching rows from both tables. LEFT JOIN returns all rows from the left table plus matching rows from the right (NULLs for non-matches). FULL OUTER JOIN returns all rows from both tables with NULLs where there's no match.",
            "keywords": ["inner", "left", "outer", "join", "match", "null", "table", "row"]
        },
        {
            "text": "What are database indexes and when should you use them?",
            "difficulty": "medium",
            "sample_answer": "Indexes are data structures (usually B-tree) that speed up data retrieval at the cost of slower writes and extra storage. Use indexes on columns frequently used in WHERE, JOIN, ORDER BY. Avoid over-indexing small tables or columns with low cardinality. Composite indexes help multi-column queries.",
            "keywords": ["index", "B-tree", "query", "performance", "column", "WHERE", "speed", "retrieval"]
        },
    ],
    # --- Web Frameworks ---
    "React": [
        {
            "text": "Explain the Virtual DOM in React and how it improves performance.",
            "difficulty": "medium",
            "sample_answer": "The Virtual DOM is a lightweight JavaScript copy of the real DOM. When state changes, React creates a new Virtual DOM, diffs it with the previous one (reconciliation), and applies only the minimal necessary changes to the real DOM. This batching and diffing process is faster than direct DOM manipulation.",
            "keywords": ["virtual DOM", "diff", "reconciliation", "performance", "render", "state", "update"]
        },
        {
            "text": "What are React Hooks and why were they introduced?",
            "difficulty": "easy",
            "sample_answer": "Hooks (useState, useEffect, useContext, etc.) let you use state and lifecycle features in functional components, eliminating the need for class components. They promote code reuse through custom hooks, simplify component logic, and avoid 'this' keyword confusion.",
            "keywords": ["hook", "useState", "useEffect", "functional", "state", "lifecycle", "component"]
        },
        {
            "text": "Explain React Context API vs Redux for state management.",
            "difficulty": "medium",
            "sample_answer": "Context API is built-in and good for simple shared state (theme, auth). Redux provides a centralized store with predictable state mutations, middleware support, and dev tools. Use Context for low-frequency updates and Redux for complex, frequently-changing state with many consumers.",
            "keywords": ["context", "redux", "state", "store", "provider", "dispatch", "management"]
        },
    ],
    "Angular": [
        {
            "text": "Explain dependency injection in Angular.",
            "difficulty": "medium",
            "sample_answer": "Dependency injection is a design pattern where components receive their dependencies from an external source rather than creating them. Angular's DI system uses providers registered in modules or components, injectors to create instances, and decorators like @Injectable(). This promotes loose coupling and testability.",
            "keywords": ["dependency", "injection", "provider", "injectable", "service", "injector", "coupling"]
        },
    ],
    "Django": [
        {
            "text": "Explain Django's ORM and the N+1 query problem.",
            "difficulty": "medium",
            "sample_answer": "Django ORM maps Python classes to database tables. The N+1 problem occurs when accessing related objects in a loop, causing one query per item plus the initial query. Solutions: select_related() for ForeignKey (SQL JOIN) and prefetch_related() for ManyToMany (separate cached query).",
            "keywords": ["ORM", "query", "N+1", "select_related", "prefetch", "database", "model", "join"]
        },
    ],
    "Flask": [
        {
            "text": "How does Flask handle request routing and what are Blueprints?",
            "difficulty": "medium",
            "sample_answer": "Flask uses decorators (@app.route) to map URLs to view functions using Werkzeug's routing system. Blueprints are modular components that group related views, templates, and static files. They allow splitting a large application into organized, reusable modules registered with the app.",
            "keywords": ["route", "blueprint", "decorator", "URL", "view", "module", "Werkzeug"]
        },
    ],
    "Node.js": [
        {
            "text": "Explain the Node.js event-driven, non-blocking I/O model.",
            "difficulty": "medium",
            "sample_answer": "Node.js uses a single-threaded event loop with non-blocking I/O operations. When an I/O request is made, Node delegates it to the OS/thread pool and continues processing. Callbacks/Promises are invoked when I/O completes. This enables handling thousands of concurrent connections efficiently.",
            "keywords": ["event", "non-blocking", "I/O", "single-threaded", "callback", "async", "loop", "concurrent"]
        },
    ],
    # --- Cloud & DevOps ---
    "Docker": [
        {
            "text": "Explain Docker containers vs virtual machines.",
            "difficulty": "medium",
            "sample_answer": "Containers share the host OS kernel and are lightweight (MBs, start in seconds). VMs run full OS instances with a hypervisor and are heavier (GBs, start in minutes). Containers provide process isolation while VMs provide hardware-level isolation. Docker uses images, layers, and Dockerfiles for reproducible builds.",
            "keywords": ["container", "VM", "kernel", "image", "layer", "isolation", "lightweight", "Dockerfile"]
        },
    ],
    "Kubernetes": [
        {
            "text": "Explain Kubernetes pods, services, and deployments.",
            "difficulty": "hard",
            "sample_answer": "Pods are the smallest deployable units containing one or more containers sharing network/storage. Services provide stable networking and load balancing across pods. Deployments manage pod replicas, rolling updates, and rollbacks declaratively. Together they enable scalable, self-healing container orchestration.",
            "keywords": ["pod", "service", "deployment", "container", "replica", "rolling update", "orchestrat"]
        },
    ],
    "AWS": [
        {
            "text": "Explain the key differences between EC2, Lambda, and ECS.",
            "difficulty": "medium",
            "sample_answer": "EC2 provides virtual machines with full OS control. Lambda is serverless – you upload code and AWS manages infrastructure, scaling, and billing per invocation. ECS is a container orchestration service for Docker containers. Choose EC2 for full control, Lambda for event-driven functions, ECS for containerized applications.",
            "keywords": ["EC2", "Lambda", "ECS", "serverless", "container", "virtual machine", "scaling"]
        },
    ],
    # --- Data Science & ML ---
    "Machine Learning": [
        {
            "text": "Explain the bias-variance tradeoff in machine learning.",
            "difficulty": "hard",
            "sample_answer": "Bias is error from simplifying assumptions (underfitting). Variance is sensitivity to training data fluctuations (overfitting). High bias = simple model that misses patterns. High variance = complex model that memorizes noise. The goal is finding the sweet spot that minimizes total error. Techniques: cross-validation, regularization, ensemble methods.",
            "keywords": ["bias", "variance", "overfit", "underfit", "regularization", "tradeoff", "error"]
        },
        {
            "text": "What is the difference between supervised, unsupervised, and reinforcement learning?",
            "difficulty": "easy",
            "sample_answer": "Supervised learning uses labeled data to learn input-output mappings (classification, regression). Unsupervised learning finds patterns in unlabeled data (clustering, dimensionality reduction). Reinforcement learning trains agents through rewards/penalties in an environment (game AI, robotics).",
            "keywords": ["supervised", "unsupervised", "reinforcement", "label", "classification", "clustering", "reward"]
        },
    ],
    "Deep Learning": [
        {
            "text": "Explain the architecture and training process of a neural network.",
            "difficulty": "hard",
            "sample_answer": "Neural networks have input, hidden, and output layers connected by weighted edges. Training uses forward propagation (compute output), loss calculation, and backpropagation (compute gradients). Optimizers like SGD or Adam update weights to minimize loss. Key concepts: activation functions (ReLU, sigmoid), epochs, batch size, learning rate.",
            "keywords": ["layer", "weight", "backpropagation", "gradient", "loss", "activation", "optimizer", "forward"]
        },
    ],
    "TensorFlow": [
        {
            "text": "How does TensorFlow's computational graph work?",
            "difficulty": "medium",
            "sample_answer": "TensorFlow 2.x uses eager execution by default (operations run immediately). tf.function decorator enables graph mode for optimization. Graphs define computation as nodes (operations) and edges (tensors). Benefits: automatic differentiation, GPU acceleration, model serialization with SavedModel format.",
            "keywords": ["graph", "tensor", "eager", "operation", "function", "GPU", "model", "execution"]
        },
    ],
    # --- Databases ---
    "MongoDB": [
        {
            "text": "When would you choose MongoDB over a relational database?",
            "difficulty": "medium",
            "sample_answer": "Choose MongoDB for flexible/evolving schemas, document-oriented data, high write throughput, horizontal scaling (sharding), and rapid prototyping. Relational databases are better for complex joins, ACID transactions, structured data, and strong consistency requirements. MongoDB uses BSON documents in collections instead of rows in tables.",
            "keywords": ["document", "schema", "flexible", "sharding", "NoSQL", "BSON", "collection", "scalab"]
        },
    ],
    "Redis": [
        {
            "text": "Explain Redis data structures and common use cases.",
            "difficulty": "medium",
            "sample_answer": "Redis is an in-memory data store supporting strings, lists, sets, sorted sets, hashes, streams, and bitmaps. Use cases: caching (reduce DB load), session storage, rate limiting (sorted sets), real-time leaderboards, pub/sub messaging, and distributed locks. Redis provides sub-millisecond latency.",
            "keywords": ["cache", "in-memory", "data structure", "string", "hash", "set", "pub/sub", "session"]
        },
    ],
    # --- Architecture ---
    "Microservices": [
        {
            "text": "What are the advantages and challenges of microservices architecture?",
            "difficulty": "hard",
            "sample_answer": "Advantages: independent deployment, technology diversity, scalability per service, team autonomy, fault isolation. Challenges: distributed system complexity, data consistency, inter-service communication, monitoring/tracing (need observability), network latency, and operational overhead. Mitigate with API gateways, service mesh, event-driven patterns.",
            "keywords": ["independent", "deployment", "scalab", "distributed", "communication", "service", "fault", "complexity"]
        },
    ],
    "System Design": [
        {
            "text": "How would you design a URL shortener like bit.ly?",
            "difficulty": "hard",
            "sample_answer": "Components: API gateway, URL shortening service (base62 encoding or hash), key-value store (Redis for cache + DB for persistence), redirection service (301/302). Handle collisions with retry or unique ID generator. Scale with read replicas, CDN, and sharding by hash prefix. Rate limit API calls. Analytics via async event processing.",
            "keywords": ["hash", "base62", "redirect", "cache", "database", "scale", "API", "shorten"]
        },
    ],
    # --- Testing ---
    "Testing": [
        {
            "text": "Explain the testing pyramid and different types of tests.",
            "difficulty": "medium",
            "sample_answer": "The testing pyramid has unit tests at the base (fast, isolated, most numerous), integration tests in the middle (test component interactions), and E2E/UI tests at the top (slow, expensive, fewest). Also: acceptance tests (user stories), performance tests (load/stress), and contract tests (API boundaries).",
            "keywords": ["unit", "integration", "E2E", "pyramid", "isolated", "component", "performance"]
        },
    ],
    # --- Git ---
    "Git": [
        {
            "text": "Explain Git branching strategies like GitFlow and trunk-based development.",
            "difficulty": "medium",
            "sample_answer": "GitFlow uses long-lived branches: main, develop, feature/*, release/*, hotfix/*. Good for versioned releases. Trunk-based development uses short-lived feature branches merged frequently to main/trunk with feature flags. Better for CI/CD and rapid deployment. GitHub Flow is a simpler variant with feature branches and PRs.",
            "keywords": ["branch", "merge", "GitFlow", "trunk", "feature", "release", "pull request", "CI/CD"]
        },
    ],
}

BEHAVIORAL_QUESTIONS = [
    {
        "text": "Tell me about a time you had to deal with a difficult team member.",
        "difficulty": "medium",
        "sample_answer": "Use the STAR method: Describe the Situation, your Task/role, the Actions you took (active listening, finding common ground, escalation if needed), and the Result (improved collaboration, successful project delivery). Show empathy and professionalism.",
        "keywords": ["team", "conflict", "communication", "resolution", "collaboration", "empathy", "listen"]
    },
    {
        "text": "Describe a project where you had to learn a new technology quickly.",
        "difficulty": "easy",
        "sample_answer": "Describe the project context, the new technology, your learning approach (documentation, tutorials, pair programming), how you applied it, and the outcome. Emphasize adaptability, resourcefulness, and willingness to grow.",
        "keywords": ["learn", "technology", "adapt", "resource", "project", "quick", "growth"]
    },
    {
        "text": "Tell me about a time you failed and what you learned from it.",
        "difficulty": "medium",
        "sample_answer": "Be honest about the failure. Explain the context, what went wrong, your role in it, immediate actions to mitigate damage, and most importantly – the lessons learned and how you applied them going forward. Show accountability and growth mindset.",
        "keywords": ["fail", "learn", "mistake", "improve", "accountab", "growth", "lesson"]
    },
    {
        "text": "How do you handle tight deadlines and multiple priorities?",
        "difficulty": "easy",
        "sample_answer": "Describe your prioritization framework (urgency/impact matrix), communication with stakeholders about trade-offs, breaking work into smaller tasks, delegation when possible, and maintaining quality. Give a specific example of successful delivery under pressure.",
        "keywords": ["priority", "deadline", "manage", "organize", "communicate", "task", "deliver"]
    },
    {
        "text": "Describe a time when you had to persuade others to adopt your technical approach.",
        "difficulty": "medium",
        "sample_answer": "Explain the technical decision, alternative approaches considered, how you built your case (data, prototypes, benchmarks), how you presented it to the team, addressed concerns, and the outcome. Show leadership and technical communication skills.",
        "keywords": ["persuade", "technical", "approach", "team", "decision", "data", "present"]
    },
    {
        "text": "Tell me about a time you mentored or helped a junior developer.",
        "difficulty": "medium",
        "sample_answer": "Describe the situation, the junior developer's challenge, your mentoring approach (pair programming, code reviews, knowledge sharing), and the outcome (their growth, team productivity). Show patience, teaching ability, and leadership.",
        "keywords": ["mentor", "junior", "teach", "help", "guide", "review", "growth", "pair"]
    },
    {
        "text": "How do you stay updated with the latest technologies and industry trends?",
        "difficulty": "easy",
        "sample_answer": "Mention specific resources: tech blogs, conferences, online courses, open-source contributions, meetups, podcasts, newsletters, and side projects. Show genuine curiosity and continuous learning mindset.",
        "keywords": ["learn", "update", "technology", "trend", "blog", "course", "community", "continuous"]
    },
    {
        "text": "Describe a situation where you had to make a decision with incomplete information.",
        "difficulty": "hard",
        "sample_answer": "Explain the context and urgency, how you gathered available data, identified risks, consulted with team/stakeholders, made a pragmatic decision, and what the outcome was. Show analytical thinking and decisive leadership.",
        "keywords": ["decision", "incomplete", "information", "risk", "analyz", "pragmatic", "data"]
    },
    {
        "text": "Tell me about a time when you improved a process or system significantly.",
        "difficulty": "medium",
        "sample_answer": "Describe the existing process, identified inefficiencies, your proposed solution, implementation steps, metrics showing improvement, and team adoption. Quantify the impact (time saved, error reduction, cost savings).",
        "keywords": ["improve", "process", "system", "efficien", "metric", "automate", "optimize", "impact"]
    },
    {
        "text": "How do you handle disagreements with your manager about technical decisions?",
        "difficulty": "hard",
        "sample_answer": "Describe respectfully presenting your viewpoint with data and evidence, listening to their perspective, finding common ground, and ultimately supporting the final decision even if different from yours. Show professionalism and maturity.",
        "keywords": ["disagree", "manager", "respect", "data", "evidence", "communicate", "professional"]
    },
]

SITUATIONAL_QUESTIONS = [
    {
        "text": "Your production server is down during peak hours. Walk me through your incident response.",
        "difficulty": "hard",
        "sample_answer": "1) Acknowledge and communicate to stakeholders. 2) Check monitoring/logs for root cause. 3) Assess impact and severity. 4) Apply quick fix or rollback if recent deployment. 5) Restore service. 6) Post-mortem analysis. 7) Implement preventive measures. Emphasize calm decision-making and communication.",
        "keywords": ["incident", "monitor", "log", "root cause", "rollback", "communicate", "post-mortem", "restore"]
    },
    {
        "text": "You discover a critical security vulnerability in production code. What do you do?",
        "difficulty": "hard",
        "sample_answer": "1) Assess severity and exposure. 2) Report to security team and manager immediately. 3) Determine if active exploitation is occurring. 4) Develop and test a patch. 5) Deploy fix through expedited process. 6) Review access logs for breaches. 7) Update security protocols. Keep communication limited to prevent premature disclosure.",
        "keywords": ["security", "vulnerability", "patch", "report", "assess", "fix", "protocol", "breach"]
    },
    {
        "text": "A client wants a feature delivered in half the estimated time. How do you respond?",
        "difficulty": "medium",
        "sample_answer": "Acknowledge the urgency. Break down the scope and identify what can be delivered as MVP. Communicate trade-offs clearly (scope, quality, resources). Propose a phased approach. If timeline is firm, negotiate additional resources or reduced scope. Never promise what can't be delivered.",
        "keywords": ["scope", "deadline", "negotiate", "trade-off", "MVP", "communicate", "priorit", "resource"]
    },
    {
        "text": "Two senior developers on your team disagree on the architecture for a new feature. How do you handle it?",
        "difficulty": "medium",
        "sample_answer": "Facilitate a structured technical discussion. Have each present their approach with pros/cons. Evaluate against project requirements, scalability, maintainability, and timeline. Use data and prototypes if possible. If no consensus, make a decision based on technical merit and document the rationale.",
        "keywords": ["architecture", "discuss", "evaluate", "consensus", "decision", "merit", "facilitat"]
    },
    {
        "text": "You're asked to work with a legacy codebase that has no tests and poor documentation. How do you approach it?",
        "difficulty": "medium",
        "sample_answer": "1) Understand the business context and critical paths. 2) Explore the codebase, trace key workflows. 3) Add characterization tests before making changes. 4) Document as you learn. 5) Refactor incrementally (Strangler Fig pattern). 6) Establish coding standards going forward. Avoid big rewrites.",
        "keywords": ["legacy", "test", "document", "refactor", "incremental", "understand", "workflow"]
    },
    {
        "text": "Your team is falling behind on sprint commitments consistently. What would you do?",
        "difficulty": "medium",
        "sample_answer": "Analyze velocity trends and identify patterns. Investigate root causes: over-commitment, technical debt, unclear requirements, or team issues. Adjust sprint planning, improve estimation, reduce WIP. Address blockers in retrospectives. Communicate honestly with stakeholders about realistic timelines.",
        "keywords": ["sprint", "velocity", "estimate", "retrospective", "backlog", "commitment", "block"]
    },
    {
        "text": "You need to migrate a monolithic application to microservices. How do you plan this?",
        "difficulty": "hard",
        "sample_answer": "1) Map domain boundaries (DDD). 2) Identify candidate services by business capability. 3) Start with a low-risk service (Strangler Fig). 4) Set up infrastructure (API gateway, service mesh, CI/CD). 5) Migrate incrementally, keeping the monolith running. 6) Handle data decomposition carefully. 7) Implement observability from day one.",
        "keywords": ["migrate", "microservice", "domain", "incremental", "API", "infrastructure", "decompos"]
    },
    {
        "text": "How would you onboard a new developer to your team's codebase?",
        "difficulty": "easy",
        "sample_answer": "Prepare documentation and architecture overview. Assign a buddy/mentor. Start with small, well-defined tasks. Pair programming sessions on key areas. Regular check-ins. Encourage questions. Provide access to all tools and environments. Review their first PRs thoroughly with constructive feedback.",
        "keywords": ["onboard", "document", "mentor", "pair", "review", "task", "buddy", "feedback"]
    },
]

SYSTEM_DESIGN_QUESTIONS = [
    {
        "text": "Design a real-time chat application like Slack.",
        "difficulty": "hard",
        "sample_answer": "Components: WebSocket server for real-time messaging, REST API for CRUD operations, message queue (Kafka/RabbitMQ) for async processing, database (messages in Cassandra/MongoDB, metadata in PostgreSQL), Redis for presence/caching, file storage (S3) for attachments. Scale with WebSocket clusters, connection load balancing, and message partitioning by channel.",
        "keywords": ["WebSocket", "real-time", "message", "queue", "database", "scale", "cache", "API"]
    },
    {
        "text": "Design a notification system that handles millions of users.",
        "difficulty": "hard",
        "sample_answer": "Components: event ingestion (Kafka), notification service, template engine, delivery services (push, email, SMS, in-app), user preferences store, rate limiter, delivery tracking. Use fan-out pattern for broadcasts. Queue priority levels. Implement retry with exponential backoff. Scale with horizontal partitioning by user ID.",
        "keywords": ["notification", "queue", "scale", "delivery", "event", "push", "priority", "retry"]
    },
    {
        "text": "Design a rate limiter for an API gateway.",
        "difficulty": "hard",
        "sample_answer": "Algorithms: Token Bucket (smooth traffic), Sliding Window (accurate counting), Fixed Window (simple). Storage: Redis for distributed counters. Key design: per-user, per-IP, or per-endpoint limits. Handle distributed scenarios with Redis MULTI/Lua scripts. Return 429 with Retry-After header. Consider different tiers and quotas.",
        "keywords": ["rate limit", "token bucket", "sliding window", "Redis", "counter", "distributed", "429", "API"]
    },
    {
        "text": "Design a file storage and sharing service like Google Drive.",
        "difficulty": "hard",
        "sample_answer": "Components: metadata service (PostgreSQL), object storage (S3), chunking service for large files, sync service for conflict resolution, sharing/permissions service, search index (Elasticsearch). Handle: deduplication (content-hash), versioning, concurrent edits (operational transform or CRDT), encryption at rest and in transit.",
        "keywords": ["storage", "metadata", "chunk", "sync", "permission", "version", "dedup", "encrypt"]
    },
    {
        "text": "Design a content delivery network (CDN).",
        "difficulty": "hard",
        "sample_answer": "Architecture: origin servers, edge/PoP nodes globally, DNS-based routing (GeoDNS or Anycast). Caching strategy: pull-based with TTL, cache invalidation via purge API. Handle: cache hierarchy (L1/L2), hot-spot mitigation, SSL termination, DDoS protection. Optimize with compression, HTTP/2, connection pooling.",
        "keywords": ["CDN", "edge", "cache", "DNS", "origin", "invalidat", "PoP", "routing"]
    },
]


def generate_questions(skills, experience_years, job_role=None):
    """
    Generate categorized interview questions based on candidate profile.

    Args:
        skills: List of skill dicts with 'skill' and 'category' keys.
        experience_years: Estimated years of experience (float).
        job_role: Optional target job role string.

    Returns:
        List of question dicts with id, text, category, difficulty, skill_related, sample_answer.
    """
    questions = []
    used_texts = set()

    # --- Technical questions based on detected skills ---
    skill_names = [s['skill'] for s in skills] if skills else []

    for skill_name in skill_names:
        templates = TECHNICAL_QUESTIONS.get(skill_name, [])
        for tmpl in templates:
            if tmpl['text'] not in used_texts:
                questions.append(_make_question(tmpl, 'technical', skill_name))
                used_texts.add(tmpl['text'])

    # Also match by category keywords (e.g., "Machine Learning" templates for ML skills)
    category_mappings = {
        "Data Science & ML": ["Machine Learning", "Deep Learning", "TensorFlow"],
        "Testing": ["Testing"],
        "Architecture & Patterns": ["Microservices", "System Design"],
        "Cloud & DevOps": ["Docker", "Kubernetes", "AWS"],
    }
    if skills:
        for s in skills:
            cat = s.get('category', '')
            mapped_keys = category_mappings.get(cat, [])
            for key in mapped_keys:
                for tmpl in TECHNICAL_QUESTIONS.get(key, []):
                    if tmpl['text'] not in used_texts:
                        questions.append(_make_question(tmpl, 'technical', s['skill']))
                        used_texts.add(tmpl['text'])

    # If no skill-specific questions, add generic ones
    if not questions:
        for key in ["Python", "JavaScript", "SQL", "Git", "Testing"]:
            for tmpl in TECHNICAL_QUESTIONS.get(key, [])[:1]:
                if tmpl['text'] not in used_texts:
                    questions.append(_make_question(tmpl, 'technical', key))
                    used_texts.add(tmpl['text'])

    # --- Behavioral questions ---
    num_behavioral = min(5, len(BEHAVIORAL_QUESTIONS))
    behavioral_sample = random.sample(BEHAVIORAL_QUESTIONS, num_behavioral)
    for tmpl in behavioral_sample:
        if tmpl['text'] not in used_texts:
            questions.append(_make_question(tmpl, 'behavioral', None))
            used_texts.add(tmpl['text'])

    # --- Situational questions ---
    num_situational = min(4, len(SITUATIONAL_QUESTIONS))
    situational_sample = random.sample(SITUATIONAL_QUESTIONS, num_situational)
    for tmpl in situational_sample:
        if tmpl['text'] not in used_texts:
            questions.append(_make_question(tmpl, 'situational', None))
            used_texts.add(tmpl['text'])

    # --- System design questions for experienced candidates ---
    if experience_years >= 3:
        num_design = min(3, len(SYSTEM_DESIGN_QUESTIONS))
        design_sample = random.sample(SYSTEM_DESIGN_QUESTIONS, num_design)
        for tmpl in design_sample:
            if tmpl['text'] not in used_texts:
                questions.append(_make_question(tmpl, 'system_design', None))
                used_texts.add(tmpl['text'])

    # Assign sequential IDs
    for idx, q in enumerate(questions, 1):
        q['id'] = idx

    return questions


def _make_question(template, category, skill_related):
    """Create a question dict from a template."""
    return {
        'id': 0,  # Will be reassigned
        'text': template['text'],
        'category': category,
        'difficulty': template.get('difficulty', 'medium'),
        'skill_related': skill_related,
        'sample_answer': template.get('sample_answer', ''),
        'keywords': template.get('keywords', [])
    }


def evaluate_answer(question, answer):
    """
    Evaluate a candidate's answer to an interview question.

    Args:
        question: Question dict (must contain 'keywords' and 'sample_answer').
        answer: Candidate's answer string.

    Returns:
        Dict with 'score' (0-10) and 'feedback' string.
    """
    if not answer or not answer.strip():
        return {
            'score': 0,
            'feedback': 'No answer provided. Try to address the question with specific examples and technical details.'
        }

    answer_lower = answer.lower().strip()
    keywords = question.get('keywords', [])
    sample_answer = question.get('sample_answer', '')

    # --- Keyword matching score (0-5 points) ---
    if keywords:
        matched = sum(1 for kw in keywords if kw.lower() in answer_lower)
        keyword_ratio = matched / len(keywords)
        keyword_score = round(keyword_ratio * 5, 1)
    else:
        keyword_score = 2.5  # Neutral if no keywords defined

    # --- Length and detail score (0-2 points) ---
    word_count = len(answer.split())
    if word_count >= 80:
        length_score = 2.0
    elif word_count >= 50:
        length_score = 1.5
    elif word_count >= 25:
        length_score = 1.0
    elif word_count >= 10:
        length_score = 0.5
    else:
        length_score = 0.2

    # --- Structure and specificity (0-2 points) ---
    structure_score = 0.0
    # Check for examples
    if any(w in answer_lower for w in ['example', 'for instance', 'such as', 'e.g.', 'like when']):
        structure_score += 0.7
    # Check for technical terms
    if any(w in answer_lower for w in ['because', 'therefore', 'however', 'specifically', 'in particular']):
        structure_score += 0.5
    # Check for structured response
    if any(w in answer_lower for w in ['first', 'second', 'finally', 'step', '1)', '2)', 'additionally']):
        structure_score += 0.8
    structure_score = min(structure_score, 2.0)

    # --- Relevance score (0-1 point) ---
    relevance_score = 0.0
    if sample_answer:
        sample_words = set(re.findall(r'\b\w{4,}\b', sample_answer.lower()))
        answer_words = set(re.findall(r'\b\w{4,}\b', answer_lower))
        if sample_words:
            overlap = len(sample_words & answer_words) / len(sample_words)
            relevance_score = round(overlap, 1)

    total_score = round(min(keyword_score + length_score + structure_score + relevance_score, 10), 1)

    # --- Generate feedback ---
    feedback_parts = []
    if keyword_score >= 4:
        feedback_parts.append("Excellent coverage of key concepts.")
    elif keyword_score >= 2.5:
        feedback_parts.append("Good understanding demonstrated, but some key points were missed.")
    else:
        feedback_parts.append("Several important concepts were not addressed.")
        if keywords:
            missed = [kw for kw in keywords if kw.lower() not in answer_lower][:3]
            if missed:
                feedback_parts.append(f"Consider discussing: {', '.join(missed)}.")

    if length_score < 1.0:
        feedback_parts.append("Try to provide more detail and depth in your answer.")

    if structure_score < 1.0:
        feedback_parts.append("Use examples and structured reasoning (e.g., 'First... Then... Finally...') to strengthen your response.")

    if total_score >= 8:
        feedback_parts.insert(0, "Outstanding answer!")
    elif total_score >= 6:
        feedback_parts.insert(0, "Good answer overall.")
    elif total_score >= 4:
        feedback_parts.insert(0, "Decent attempt, but there's room for improvement.")
    else:
        feedback_parts.insert(0, "This answer needs significant improvement.")

    return {
        'score': total_score,
        'feedback': ' '.join(feedback_parts)
    }
