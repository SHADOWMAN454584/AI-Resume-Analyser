"""
NLP engine for skill extraction, entity recognition, and experience estimation.
Uses spaCy for NER and pattern matching, plus keyword-based skill detection.
"""
import re

try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        nlp = None
except ImportError:
    nlp = None

# ---------------------------------------------------------------------------
# Comprehensive skills database – 300+ skills organized by category
# ---------------------------------------------------------------------------
SKILLS_DATABASE = {
    "Programming Languages": [
        "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#",
        "Go", "Golang", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "R",
        "MATLAB", "Scala", "Perl", "Haskell", "Erlang", "Elixir", "Lua",
        "Dart", "Objective-C", "Assembly", "COBOL", "Fortran", "Julia",
        "Groovy", "Clojure", "F#", "Visual Basic", "VB.NET", "Shell",
        "Bash", "PowerShell", "SQL", "PL/SQL", "T-SQL", "Solidity",
        "VHDL", "Verilog"
    ],
    "Web Frameworks": [
        "React", "React.js", "Angular", "AngularJS", "Vue", "Vue.js",
        "Svelte", "Next.js", "Nuxt.js", "Gatsby", "Django", "Flask",
        "FastAPI", "Spring", "Spring Boot", "Express", "Express.js",
        "NestJS", "Ruby on Rails", "Rails", "Laravel", "Symfony",
        "ASP.NET", "ASP.NET Core", "Blazor", "Gin", "Echo", "Fiber",
        "Actix", "Rocket", "Phoenix", "Remix", "Astro", "SvelteKit",
        "jQuery", "Bootstrap", "Tailwind CSS", "Material UI", "Chakra UI",
        "Ant Design", "Semantic UI"
    ],
    "Databases": [
        "MySQL", "PostgreSQL", "SQLite", "MariaDB", "Oracle", "Oracle DB",
        "SQL Server", "Microsoft SQL Server", "MongoDB", "Cassandra",
        "Redis", "Memcached", "DynamoDB", "CouchDB", "CouchBase",
        "Neo4j", "ArangoDB", "InfluxDB", "TimescaleDB", "Elasticsearch",
        "Firebase", "Firestore", "Supabase", "HBase", "Snowflake",
        "BigQuery", "Redshift", "Amazon RDS", "CosmosDB", "Azure SQL"
    ],
    "Cloud & DevOps": [
        "AWS", "Amazon Web Services", "Azure", "Microsoft Azure",
        "GCP", "Google Cloud", "Google Cloud Platform",
        "Docker", "Kubernetes", "K8s", "Terraform", "Ansible",
        "Puppet", "Chef", "Jenkins", "CircleCI", "Travis CI",
        "GitHub Actions", "GitLab CI", "Azure DevOps", "ArgoCD",
        "Helm", "Istio", "Prometheus", "Grafana", "Datadog",
        "New Relic", "Splunk", "ELK Stack", "Logstash", "Kibana",
        "Vagrant", "Packer", "Consul", "Vault", "Nginx", "Apache",
        "HAProxy", "Cloudflare", "Heroku", "Vercel", "Netlify",
        "DigitalOcean", "Linode", "OpenStack", "VMware",
        "CI/CD", "Continuous Integration", "Continuous Deployment",
        "Infrastructure as Code", "IaC", "Serverless",
        "AWS Lambda", "Azure Functions", "Cloud Functions",
        "S3", "EC2", "ECS", "EKS", "Fargate", "CloudFormation",
        "AWS CDK", "Route 53", "CloudFront", "API Gateway",
        "SQS", "SNS", "Kinesis", "Step Functions"
    ],
    "Data Science & ML": [
        "TensorFlow", "PyTorch", "Keras", "scikit-learn", "sklearn",
        "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn", "Plotly",
        "XGBoost", "LightGBM", "CatBoost", "OpenCV", "NLTK", "spaCy",
        "Hugging Face", "Transformers", "BERT", "GPT", "LLM",
        "Large Language Models", "Deep Learning", "Machine Learning",
        "Neural Networks", "CNN", "RNN", "LSTM", "GAN",
        "Reinforcement Learning", "Computer Vision", "NLP",
        "Natural Language Processing", "MLflow", "Kubeflow",
        "Apache Spark", "PySpark", "Hadoop", "MapReduce", "Hive",
        "Pig", "Airflow", "Apache Kafka", "Flink", "Beam",
        "Data Mining", "Feature Engineering", "Model Deployment",
        "A/B Testing", "Statistical Analysis", "Regression",
        "Classification", "Clustering", "Dimensionality Reduction",
        "Time Series Analysis", "Recommendation Systems",
        "Jupyter", "Jupyter Notebook", "Google Colab",
        "Tableau", "Power BI", "Looker", "D3.js", "Apache Superset",
        "Databricks", "Snowpark", "dbt", "Apache Iceberg",
        "MLOps", "Data Pipeline", "ETL", "Data Warehousing",
        "Data Lake", "Data Mesh", "Data Governance"
    ],
    "Mobile Development": [
        "React Native", "Flutter", "Dart", "SwiftUI", "UIKit",
        "Jetpack Compose", "Android SDK", "iOS SDK", "Xamarin",
        "Ionic", "Cordova", "PhoneGap", "Expo", "Capacitor",
        "Kotlin Multiplatform", "MAUI", ".NET MAUI"
    ],
    "Testing": [
        "Jest", "Mocha", "Chai", "Cypress", "Selenium", "Playwright",
        "Puppeteer", "JUnit", "TestNG", "pytest", "unittest",
        "RSpec", "PHPUnit", "Enzyme", "React Testing Library",
        "Vitest", "Karma", "Jasmine", "Postman", "SoapUI",
        "Load Testing", "Performance Testing", "Unit Testing",
        "Integration Testing", "E2E Testing", "TDD", "BDD",
        "Test Driven Development", "Behavior Driven Development",
        "QA", "Quality Assurance", "Appium", "Robot Framework",
        "Cucumber", "JMeter", "Gatling", "Locust"
    ],
    "Tools & Platforms": [
        "Git", "GitHub", "GitLab", "Bitbucket", "SVN",
        "Jira", "Confluence", "Trello", "Asana", "Notion",
        "Slack", "Microsoft Teams", "Figma", "Sketch", "Adobe XD",
        "InVision", "Zeplin", "Storybook",
        "VS Code", "Visual Studio", "IntelliJ", "Eclipse", "PyCharm",
        "Vim", "Emacs", "Sublime Text",
        "Linux", "Unix", "Windows Server", "macOS",
        "npm", "yarn", "pnpm", "pip", "Maven", "Gradle",
        "Webpack", "Vite", "Rollup", "Parcel", "esbuild",
        "Babel", "ESLint", "Prettier", "SonarQube",
        "Swagger", "OpenAPI", "GraphQL", "REST API", "gRPC",
        "WebSocket", "Socket.IO", "RabbitMQ", "ActiveMQ",
        "ZeroMQ", "MQTT", "Apache Camel",
        "Stripe", "PayPal", "Twilio", "SendGrid", "Auth0",
        "Okta", "Keycloak", "OAuth", "OAuth2", "OpenID Connect",
        "SAML", "JWT", "LDAP", "Active Directory"
    ],
    "Architecture & Patterns": [
        "Microservices", "Monolith", "SOA", "Event-Driven Architecture",
        "CQRS", "Event Sourcing", "Domain-Driven Design", "DDD",
        "MVC", "MVVM", "MVP", "Clean Architecture", "Hexagonal Architecture",
        "REST", "RESTful", "API Design", "System Design",
        "Design Patterns", "SOLID", "OOP", "Object-Oriented Programming",
        "Functional Programming", "Reactive Programming",
        "Message Queue", "Pub/Sub", "Load Balancing",
        "Caching", "CDN", "Rate Limiting", "Circuit Breaker",
        "Saga Pattern", "Outbox Pattern",
        "Distributed Systems", "High Availability", "Scalability",
        "Fault Tolerance", "CAP Theorem", "Eventual Consistency"
    ],
    "Security": [
        "Cybersecurity", "Information Security", "Network Security",
        "Application Security", "Penetration Testing", "Ethical Hacking",
        "OWASP", "SSL/TLS", "HTTPS", "Encryption", "Cryptography",
        "Firewall", "IDS", "IPS", "SIEM", "SOC",
        "Vulnerability Assessment", "Security Audit",
        "Compliance", "GDPR", "HIPAA", "PCI DSS", "ISO 27001",
        "Zero Trust", "IAM", "Identity and Access Management"
    ],
    "Soft Skills": [
        "Leadership", "Communication", "Teamwork", "Collaboration",
        "Problem Solving", "Problem-Solving", "Critical Thinking",
        "Time Management", "Project Management", "Agile",
        "Scrum", "Kanban", "SAFe", "Lean", "Six Sigma",
        "Mentoring", "Coaching", "Presentation Skills",
        "Stakeholder Management", "Requirements Gathering",
        "Technical Writing", "Documentation",
        "Cross-Functional Collaboration", "Remote Work",
        "Adaptability", "Creativity", "Innovation",
        "Decision Making", "Conflict Resolution",
        "Negotiation", "Client Management", "Vendor Management",
        "Strategic Planning", "Risk Management",
        "Change Management", "Process Improvement"
    ]
}

# Build a lookup dict: lowercase skill -> (original skill, category)
_SKILL_LOOKUP = {}
for _cat, _skills in SKILLS_DATABASE.items():
    for _skill in _skills:
        _SKILL_LOOKUP[_skill.lower()] = (_skill, _cat)

# Pre-compile patterns for multi-word skills (sorted longest first to match greedily)
_MULTI_WORD_SKILLS = sorted(
    [s for s in _SKILL_LOOKUP if ' ' in s or '/' in s or '.' in s or '-' in s],
    key=len,
    reverse=True
)


def extract_skills(text):
    """
    Extract skills from resume text using keyword matching and NLP.

    Args:
        text: Cleaned resume text.

    Returns:
        List of dicts with keys: skill, category, confidence.
    """
    if not text:
        return []

    text_lower = text.lower()
    found_skills = {}

    # --- Pass 1: Multi-word / special-character skills (exact substring match) ---
    for skill_lower in _MULTI_WORD_SKILLS:
        if skill_lower in text_lower:
            original, category = _SKILL_LOOKUP[skill_lower]
            if original not in found_skills:
                found_skills[original] = {
                    'skill': original,
                    'category': category,
                    'confidence': _compute_confidence(skill_lower, text_lower)
                }

    # --- Pass 2: Single-word skills (word-boundary match) ---
    for skill_lower, (original, category) in _SKILL_LOOKUP.items():
        if original in found_skills:
            continue
        if ' ' in skill_lower or '/' in skill_lower or '.' in skill_lower or '-' in skill_lower:
            continue  # Already handled in pass 1
        # Word boundary match
        pattern = r'(?<![a-zA-Z0-9])' + re.escape(skill_lower) + r'(?![a-zA-Z0-9])'
        if re.search(pattern, text_lower):
            found_skills[original] = {
                'skill': original,
                'category': category,
                'confidence': _compute_confidence(skill_lower, text_lower)
            }

    # --- Pass 3: spaCy NER – extract ORG entities and match to skills ---
    if nlp is not None:
        try:
            doc = nlp(text[:100000])  # Limit to avoid memory issues
            for ent in doc.ents:
                ent_lower = ent.text.strip().lower()
                if ent_lower in _SKILL_LOOKUP and ent.text.strip() not in found_skills:
                    original, category = _SKILL_LOOKUP[ent_lower]
                    found_skills[original] = {
                        'skill': original,
                        'category': category,
                        'confidence': min(0.95, _compute_confidence(ent_lower, text_lower) + 0.1)
                    }
        except Exception:
            pass  # NLP enhancement is optional

    return sorted(found_skills.values(), key=lambda x: (-x['confidence'], x['skill']))


def _compute_confidence(skill_lower, text_lower):
    """Compute a confidence score based on frequency and context."""
    count = text_lower.count(skill_lower)
    if count >= 5:
        return 0.95
    if count >= 3:
        return 0.90
    if count >= 2:
        return 0.80
    return 0.70


def extract_entities(text):
    """
    Extract named entities (names, emails, phones, organizations) from text.

    Args:
        text: Resume text.

    Returns:
        Dict with keys: names, emails, phones, organizations, urls.
    """
    entities = {
        'names': [],
        'emails': [],
        'phones': [],
        'organizations': [],
        'urls': []
    }

    if not text:
        return entities

    # Email
    email_pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
    entities['emails'] = list(set(re.findall(email_pattern, text)))

    # Phone (various formats)
    phone_pattern = r'(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}'
    raw_phones = re.findall(phone_pattern, text)
    entities['phones'] = list(set(p.strip() for p in raw_phones if len(re.sub(r'\D', '', p)) >= 10))

    # URLs / LinkedIn
    url_pattern = r'https?://[^\s,)>]+'
    entities['urls'] = list(set(re.findall(url_pattern, text)))

    linkedin_pattern = r'linkedin\.com/in/[a-zA-Z0-9\-_%]+'
    linkedin_matches = re.findall(linkedin_pattern, text, re.IGNORECASE)
    for lnk in linkedin_matches:
        full = f'https://www.{lnk}'
        if full not in entities['urls']:
            entities['urls'].append(full)

    # spaCy NER
    if nlp is not None:
        try:
            doc = nlp(text[:50000])
            for ent in doc.ents:
                cleaned = ent.text.strip()
                if not cleaned or len(cleaned) < 2:
                    continue
                if ent.label_ == 'PERSON' and cleaned not in entities['names']:
                    # Filter out obvious non-names
                    if not re.search(r'[@\d]', cleaned):
                        entities['names'].append(cleaned)
                elif ent.label_ == 'ORG' and cleaned not in entities['organizations']:
                    entities['organizations'].append(cleaned)
        except Exception:
            pass

    # Limit results
    entities['names'] = entities['names'][:5]
    entities['organizations'] = entities['organizations'][:20]

    return entities


def extract_experience_years(text):
    """
    Estimate total years of professional experience from resume text.

    Args:
        text: Resume text.

    Returns:
        Estimated years of experience (float).
    """
    if not text:
        return 0.0

    text_lower = text.lower()
    years = 0.0

    # Pattern 1: "X+ years of experience"
    pattern1 = r'(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|expertise|professional)'
    matches1 = re.findall(pattern1, text_lower)
    if matches1:
        years = max(years, max(float(m) for m in matches1))

    # Pattern 2: "experience: X years"
    pattern2 = r'experience\s*[:\-]\s*(\d+)\+?\s*(?:years?|yrs?)'
    matches2 = re.findall(pattern2, text_lower)
    if matches2:
        years = max(years, max(float(m) for m in matches2))

    # Pattern 3: Date ranges in experience section (e.g., "2018 - 2023", "Jan 2019 - Present")
    date_range_pattern = r'(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+)?(\d{4})\s*[-–—to]+\s*(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+)?(\d{4}|present|current|now)'
    date_matches = re.findall(date_range_pattern, text_lower)

    if date_matches:
        total_from_dates = 0.0
        current_year = 2026
        for start_str, end_str in date_matches:
            try:
                start_year = int(start_str)
                if end_str in ('present', 'current', 'now'):
                    end_year = current_year
                else:
                    end_year = int(end_str)
                diff = end_year - start_year
                if 0 < diff <= 50:
                    total_from_dates += diff
            except (ValueError, TypeError):
                continue

        if total_from_dates > 0:
            years = max(years, total_from_dates)

    # Pattern 4: "over/more than X years"
    pattern4 = r'(?:over|more than|approximately|around|nearly)\s+(\d+)\s*(?:years?|yrs?)'
    matches4 = re.findall(pattern4, text_lower)
    if matches4:
        years = max(years, max(float(m) for m in matches4))

    return round(min(years, 50.0), 1)  # Cap at 50 years
