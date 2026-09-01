from django.core.management.base import BaseCommand
from careers.models import Career, Skill, CareerSkill
from assessments.models import AssessmentCategory, Question
from roadmap.models import RoadmapTemplate, RoadmapStage
from resources.models import LearningResource
from projects.models import ProjectIdea
from interviews.models import InterviewQuestion

class Command(BaseCommand):
    help = 'Seed database'
    def handle(self, *args, **options):
        self.stdout.write('Starting seeding...')
        
        # 1. Skills
        skills_data = [
            ('Python', 'Programming', 'High-level programming language.'),
            ('Java', 'Programming', 'Object-oriented programming language.'),
            ('C++', 'Programming', 'Fast system programming language.'),
            ('JavaScript', 'Programming', 'Language of the web.'),
            ('TypeScript', 'Programming', 'Typed superset of JavaScript.'),
            ('SQL', 'Database', 'Structured query language.'),
            ('HTML5/CSS3', 'Framework', 'Web styling and markup.'),
            ('React.js', 'Framework', 'UI library.'),
            ('Django', 'Framework', 'Python web framework.'),
            ('Node.js / Express', 'Framework', 'Backend JS runtime.'),
            ('Pandas & NumPy', 'Framework', 'Data manipulation libraries.'),
            ('Scikit-Learn', 'Framework', 'Machine learning library.'),
            ('TensorFlow / PyTorch', 'Framework', 'Deep learning frameworks.'),
            ('Bootstrap & Tailwind', 'Framework', 'CSS frameworks.'),
            ('Figma', 'Domain', 'UI/UX design tool.'),
            ('PostgreSQL / MySQL', 'Database', 'Relational databases.'),
            ('MongoDB', 'Database', 'NoSQL database.'),
            ('Docker', 'Cloud_DevOps', 'Containerization platform.'),
            ('Kubernetes', 'Cloud_DevOps', 'Container orchestration.'),
            ('AWS / Azure / GCP', 'Cloud_DevOps', 'Cloud computing platforms.'),
            ('CI/CD & Git', 'Cloud_DevOps', 'Continuous integration & VCS.'),
            ('Linux & Shell Scripting', 'Cloud_DevOps', 'Operating system & bash.'),
            ('Data Structures & Algorithms', 'Core_CS', 'Core computer science algorithms.'),
            ('Machine Learning', 'Domain', 'Predictive modeling.'),
            ('Deep Learning & NLP', 'Domain', 'Neural networks & text.'),
            ('Data Visualization', 'Domain', 'Dashboards and charts.'),
            ('Network Security & Cryptography', 'Domain', 'Information security.'),
            ('Ethical Hacking & SIEM', 'Domain', 'Security operations & pen-testing.'),
            ('System Design', 'Core_CS', 'Distributed architecture.'),
            ('Statistics & Probability', 'Core_CS', 'Math foundations.'),
            ('Business Intelligence', 'Domain', 'Data-driven business decisions.'),
            ('Communication', 'Soft_Skills', 'Verbal and written clarity.'),
            ('Problem Solving', 'Soft_Skills', 'Analytical reasoning.'),
            ('Teamwork & Leadership', 'Soft_Skills', 'Collaboration & leadership.'),
            ('Logical Reasoning', 'Soft_Skills', 'Deductive logic.')
        ]
        skill_map = {}
        for name, cat, desc in skills_data:
            s, _ = Skill.objects.get_or_create(name=name, defaults={'category': cat, 'description': desc})
            skill_map[name] = s
            
        # 2. Careers
        careers_def = [
            ('Software Developer', 'Software Engineering', 'Builds scalable software systems and algorithmic services.', '₹7 - ₹18 LPA', 'Very High', 'bi-code-slash', [
                ('Data Structures & Algorithms', 8.5), ('Java', 8.0), ('Python', 7.5), ('C++', 7.0), ('SQL', 7.0), ('System Design', 6.5), ('CI/CD & Git', 7.5), ('Problem Solving', 8.5)
            ]),
            ('Data Analyst', 'Data & Analytics', 'Transforms raw data into actionable visual insights and business metrics.', '₹5 - ₹12 LPA', 'High', 'bi-bar-chart-line', [
                ('SQL', 9.0), ('Pandas & NumPy', 8.0), ('Data Visualization', 9.0), ('Statistics & Probability', 7.5), ('Business Intelligence', 8.0), ('Communication', 8.5)
            ]),
            ('Data Scientist', 'Data & Analytics', 'Builds predictive models and extracts patterns from complex datasets.', '₹9 - ₹22 LPA', 'Very High', 'bi-graph-up-arrow', [
                ('Python', 9.0), ('Statistics & Probability', 9.0), ('Machine Learning', 8.5), ('Pandas & NumPy', 8.5), ('Scikit-Learn', 8.5), ('SQL', 8.0)
            ]),
            ('Machine Learning Engineer', 'Artificial Intelligence', 'Deploys deep learning and predictive models into production systems.', '₹10 - ₹25 LPA', 'Very High', 'bi-cpu', [
                ('Python', 9.0), ('Machine Learning', 9.0), ('TensorFlow / PyTorch', 8.5), ('Scikit-Learn', 8.5), ('Data Structures & Algorithms', 8.0), ('Docker', 7.5)
            ]),
            ('AI Engineer', 'Artificial Intelligence', 'Engineers LLM, GenAI, and cognitive computing applications.', '₹12 - ₹28 LPA', 'Very High', 'bi-robot', [
                ('Python', 9.5), ('Deep Learning & NLP', 9.0), ('TensorFlow / PyTorch', 9.0), ('Machine Learning', 8.5), ('AWS / Azure / GCP', 7.5)
            ]),
            ('Web Developer', 'Web & Full Stack', 'Develops responsive client interfaces and robust API backends.', '₹6 - ₹15 LPA', 'Very High', 'bi-window-stack', [
                ('JavaScript', 9.0), ('HTML5/CSS3', 9.0), ('React.js', 8.5), ('Node.js / Express', 8.0), ('Django', 7.5), ('PostgreSQL / MySQL', 7.5)
            ]),
            ('Cybersecurity Analyst', 'Security & Infrastructure', 'Defends enterprise infrastructure and assesses vulnerabilities.', '₹8 - ₹20 LPA', 'Very High', 'bi-shield-lock', [
                ('Network Security & Cryptography', 9.0), ('Ethical Hacking & SIEM', 8.5), ('Linux & Shell Scripting', 8.5), ('Python', 7.5)
            ]),
            ('Cloud Engineer', 'Cloud & Infrastructure', 'Provisions and manages highly available cloud infrastructure.', '₹8 - ₹20 LPA', 'Very High', 'bi-cloud-check', [
                ('AWS / Azure / GCP', 9.0), ('Linux & Shell Scripting', 8.5), ('Docker', 8.0), ('Kubernetes', 7.5), ('Python', 7.0)
            ]),
            ('DevOps Engineer', 'Cloud & Infrastructure', 'Automates CI/CD build pipelines and container orchestration.', '₹9 - ₹22 LPA', 'Very High', 'bi-infinity', [
                ('CI/CD & Git', 9.0), ('Docker', 9.0), ('Kubernetes', 8.5), ('Linux & Shell Scripting', 8.5), ('AWS / Azure / GCP', 8.0)
            ]),
            ('UI/UX Developer', 'Design & Frontend', 'Creates human-centric interface prototypes and responsive frontend components.', '₹6 - ₹14 LPA', 'High', 'bi-palette', [
                ('Figma', 9.5), ('HTML5/CSS3', 9.0), ('JavaScript', 8.0), ('React.js', 8.0), ('Bootstrap & Tailwind', 8.5), ('Communication', 8.5)
            ]),
            ('Business Analyst', 'Business & Strategy', 'Aligns data metrics with organizational strategy and workflows.', '₹6 - ₹16 LPA', 'High', 'bi-briefcase', [
                ('Business Intelligence', 9.0), ('SQL', 8.0), ('Data Visualization', 8.0), ('Communication', 9.5), ('Teamwork & Leadership', 9.0)
            ])
        ]
        
        career_map = {}
        for title, cat, desc, sal, dem, icon, reqs in careers_def:
            c, _ = Career.objects.get_or_create(title=title, defaults={'category': cat, 'description': desc, 'average_salary': sal, 'market_demand': dem, 'icon_class': icon})
            career_map[title] = c
            for s_name, lvl in reqs:
                if s_name in skill_map:
                    CareerSkill.objects.get_or_create(career=c, skill=skill_map[s_name], defaults={'required_level': lvl, 'importance': 'Essential', 'weight': 1.0})
                    
        self.stdout.write('Seeded skills and careers.')

        # 3. Assessment Categories & Questions
        cat_map = {}
        for code, name, desc in [
            ('interest', 'Career & Domain Interests', 'Discover domains aligned with your passion.'),
            ('aptitude', 'Logical & Quantitative Aptitude', 'Assess mathematical and logic capabilities.'),
            ('technical', 'Core Technical & Programming', 'Test fundamental algorithms, programming, and CS.'),
            ('soft_skills', 'Communication & Workplace Skills', 'Evaluate leadership and teamwork.')
        ]:
            cat, _ = AssessmentCategory.objects.get_or_create(code=code, defaults={'name': name, 'description': desc})
            cat_map[code] = cat
            
        questions = [
            (cat_map['interest'], 'Which task sounds most enjoyable for your day-to-day work?', 'Designing frontend UX and graphics', 'Analyzing datasets and charts', 'Writing backend APIs and algorithms', 'Configuring cloud infrastructure and security', 'C', 'Measures domain preference.'),
            (cat_map['interest'], 'How do you prefer solving a problem with large amounts of data?', 'Build statistical regression & ML models', 'Create executive dashboards in BI tools', 'Write clean SQL schema & store securely', 'Build a responsive web application', 'A', 'Assesses AI/Data preference.'),
            (cat_map['interest'], 'What is your interest level in cloud servers, Docker, and CI/CD automation?', 'Extremely high - love DevOps automation', 'Moderate - as long as it deploys my code', 'Low - prefer pure UI/UX styling', 'Low - prefer business analysis', 'A', 'Evaluates cloud interest.'),
            (cat_map['interest'], 'When thinking about AI applications, what fascinates you most?', 'Building LLM agents and neural networks', 'Building UI screens for end users', 'Database indexing and storage', 'Cybersecurity defense', 'A', 'Evaluates AI specialization.'),
            (cat_map['interest'], 'How exciting do you find penetration testing and finding system security loopholes?', 'Very exciting - want to specialize in cyber defense', 'Interesting, but prefer building products', 'Neutral', 'Not interested', 'A', 'Evaluates security interest.'),
            
            (cat_map['aptitude'], 'If 5 developers complete a project in 12 days, how many days will 3 developers take?', '18 days', '20 days', '24 days', '15 days', 'B', 'Total dev-days = 60. 60 / 3 = 20 days.'),
            (cat_map['aptitude'], 'Find the missing number in the sequence: 3, 7, 15, 31, 63, ___', '127', '125', '129', '115', 'A', 'Each number is (2 * previous) + 1. 2*63 + 1 = 127.'),
            (cat_map['aptitude'], 'A speed of 90 km/h is equal to how many meters per second?', '20 m/s', '25 m/s', '30 m/s', '35 m/s', 'B', '90 * (5/18) = 25 m/s.'),
            (cat_map['aptitude'], 'All roses are flowers. Some flowers fade quickly. Therefore:', 'All roses fade quickly', 'Some roses may fade quickly', 'No roses fade quickly', 'All flowers are roses', 'B', 'Some flowers (which may include roses) fade quickly.'),
            (cat_map['aptitude'], 'If P is the brother of Q, and Q is the mother of R, how is P related to R?', 'Father', 'Maternal Uncle', 'Brother', 'Grandfather', 'B', 'P is the maternal uncle of R.'),
            
            (cat_map['technical'], 'What is the worst-case time complexity of QuickSort?', 'O(n log n)', 'O(n^2)', 'O(n)', 'O(log n)', 'B', 'QuickSort degenerates to O(n^2) when poor pivot selection occurs on sorted data.'),
            (cat_map['technical'], 'Which data structure follows the Last-In First-Out (LIFO) principle?', 'Queue', 'Stack', 'Linked List', 'Binary Tree', 'B', 'Stacks operate under LIFO order.'),
            (cat_map['technical'], 'In SQL, what is the key difference between INNER JOIN and LEFT JOIN?', 'INNER returns matching rows; LEFT returns all rows from left table plus matched rows', 'LEFT returns only unmatched rows', 'INNER modifies the table schema', 'There is no difference', 'A', 'LEFT JOIN preserves unmatched left rows with NULL values.'),
            (cat_map['technical'], 'In Python, what is the output of bool([])?', 'True', 'False', 'None', 'Error', 'B', 'Empty lists evaluate to False in boolean context.'),
            (cat_map['technical'], 'What is the primary role of a Reverse Proxy (such as Nginx)?', 'To write database queries', 'To distribute traffic, provide caching, and terminate SSL before backends', 'To format CSS styling', 'To compile C++ code', 'B', 'Nginx acts as a high-performance reverse proxy and load balancer.'),
            
            (cat_map['soft_skills'], 'How do you handle constructive criticism on your code during a pull request review?', 'Argue defensively without reading comments', 'Review the suggestions objectively, ask clarifying questions, and update the code', 'Ignore the feedback and merge anyway', 'Delete the pull request', 'B', 'Reflects collaborative learning and professionalism.'),
            (cat_map['soft_skills'], 'When leading a technical project with strict deadlines, how do you distribute tasks?', 'Keep all interesting work for yourself', 'Assess team strengths, define clear deliverables, and maintain open sprint check-ins', 'Give all tasks to the junior developer', 'Let everyone work without coordination', 'B', 'Reflects structured leadership and team empowerment.'),
            (cat_map['soft_skills'], 'How do you communicate a project delay to stakeholders?', 'Wait until after the deadline has passed', 'Proactively explain the root blockers, new realistic timeline, and mitigation strategies', 'Blame external vendors', 'Pretend the project is on track', 'B', 'Reflects transparent and mature professional communication.')
        ]
        for c, q_text, a, b, c_opt, d, corr, expl in questions:
            Question.objects.get_or_create(category=c, question_text=q_text, defaults={'option_a': a, 'option_b': b, 'option_c': c_opt, 'option_d': d, 'correct_option': corr, 'explanation': expl})
            
        # 4. Roadmaps
        for c_title, stages in [
            ('Software Developer', [
                ('Stage 1: Core Programming & OOP', 'Master Java/Python, OOP principles, and clean coding.', 4),
                ('Stage 2: DSA & Algorithmic Problem Solving', 'Binary Trees, Graphs, Dynamic Programming, and LeetCode mastery.', 6),
                ('Stage 3: Database Design & Backend Frameworks', 'Relational database schema modeling, SQL query tuning, and Django/Express.', 4),
                ('Stage 4: System Architecture & Distributed Services', 'REST APIs, caching, message queues, and Microservices.', 4),
                ('Stage 5: Production Deployment & CI/CD', 'Docker containerization, GitHub Actions pipelines, and cloud hosting.', 3)
            ]),
            ('Data Scientist', [
                ('Stage 1: Python & Exploratory Data Analysis', 'Pandas, NumPy, Matplotlib, and data wrangling.', 4),
                ('Stage 2: Statistical Modeling & Mathematics', 'Probability, hypothesis testing, and linear algebra.', 4),
                ('Stage 3: Machine Learning & Scikit-Learn', 'Supervised learning, classification, regression, and model tuning.', 5),
                ('Stage 4: Deep Learning & NLP', 'Neural networks, PyTorch, computer vision, and transformers.', 5),
                ('Stage 5: Model Deployment & MLOps', 'Serving models with FastAPI, Docker, and monitoring in production.', 4)
            ]),
            ('Web Developer', [
                ('Stage 1: Modern HTML, CSS & Responsive Design', 'Flexbox, CSS Grid, Tailwind, and Bootstrap 5 layouts.', 3),
                ('Stage 2: Modern JavaScript (ES6+)', 'Async/Await, DOM manipulation, Promises, and Fetch API.', 4),
                ('Stage 3: Frontend Framework with React.js', 'Components, hooks, state management, and SPA routing.', 5),
                ('Stage 4: Backend REST APIs with Django / Node', 'Authentication, database ORM, and API endpoints.', 4),
                ('Stage 5: Full Stack Deployment & Cloud', 'Docker, PostgreSQL, CI/CD, and production deployment.', 3)
            ]),
            ('Machine Learning Engineer', [
                ('Stage 1: Python Engineering & Linear Algebra', 'OOP Python, vector operations, and matrix algebra.', 4),
                ('Stage 2: Supervised & Unsupervised Machine Learning', 'Feature engineering, hyperparameter search, and model validation.', 5),
                ('Stage 3: Deep Neural Networks & Computer Vision / NLP', 'PyTorch, CNNs, Transformers, and Transfer Learning.', 5),
                ('Stage 4: High-Performance Model Serving', 'FastAPI, TorchServe, ONNX, and latency optimization.', 4),
                ('Stage 5: End-to-End MLOps Pipeline', 'Data drift tracking, MLflow, Docker, and automated retraining.', 4)
            ]),
            ('Cybersecurity Analyst', [
                ('Stage 1: Networking Protocols & Packet Analysis', 'TCP/IP, Wireshark, DNS, and HTTP security headers.', 4),
                ('Stage 2: Linux Administration & Shell Security', 'User privileges, firewall configuration, and bash scripting.', 4),
                ('Stage 3: Vulnerability Assessment & Pen-Testing', 'OWASP Top 10, Nmap scanning, Metasploit, and report writing.', 5),
                ('Stage 4: Cloud Infrastructure Defense', 'AWS security groups, IAM policy least-privilege, and KMS.', 4),
                ('Stage 5: SIEM Monitoring & Incident Response', 'Splunk, log analysis, threat intelligence, and remediation.', 4)
            ])
        ]:
            if c_title in career_map:
                c = career_map[c_title]
                tmpl, _ = RoadmapTemplate.objects.get_or_create(career=c, defaults={'title': f'Complete Career Track: {c.title}', 'description': f'Roadmap for {c.title}.', 'estimated_months': len(stages)})
                for idx, (st_t, st_d, weeks) in enumerate(stages, 1):
                    RoadmapStage.objects.get_or_create(template=tmpl, stage_number=idx, defaults={'title': st_t, 'description': st_d, 'estimated_weeks': weeks, 'learning_outcomes': 'Build practical portfolio projects.'})

        # 5. Resources
        for title, s_name, cat, plat, lvl, dur, desc, url, is_free in [
            ('Python for Everybody Specialization', 'Python', 'Course', 'Coursera', 'Beginner', '8 Weeks', 'Complete Python from basics to data structures.', 'https://www.coursera.org', True),
            ('Complete SQL Mastery', 'SQL', 'Course', 'Udemy', 'Beginner', '4 Weeks', 'Master SQL queries, joins, and PostgreSQL.', 'https://www.udemy.com', False),
            ('Machine Learning by Andrew Ng', 'Machine Learning', 'Course', 'Coursera', 'Intermediate', '10 Weeks', 'World-leading foundational ML course.', 'https://www.coursera.org', True),
            ('CS50 Computer Science', 'Data Structures & Algorithms', 'Course', 'edX', 'Beginner', '10 Weeks', 'Harvard introductory CS foundations.', 'https://www.edx.org', True),
            ('Full Stack React & Node Bootcamp', 'React.js', 'Course', 'Udemy', 'Intermediate', '8 Weeks', 'Build real-world full stack web applications.', 'https://www.udemy.com', False),
            ('Docker and Kubernetes Guide', 'Docker', 'Course', 'Udemy', 'Intermediate', '6 Weeks', 'Master containers and microservice orchestration.', 'https://www.udemy.com', False),
            ('AWS Solutions Architect Guide', 'AWS / Azure / GCP', 'Certification', 'A Cloud Guru', 'Intermediate', '8 Weeks', 'Comprehensive cloud architecture.', 'https://aws.amazon.com', False),
            ('Deep Learning with PyTorch', 'Deep Learning & NLP', 'Course', 'Coursera', 'Advanced', '10 Weeks', 'Build neural networks and transformer models.', 'https://www.coursera.org', True),
            ('Hands-On Machine Learning Textbook', 'Scikit-Learn', 'Book', 'O\'Reilly', 'Intermediate', 'Self-Paced', 'Essential guide to applied machine learning.', 'https://www.oreilly.com', False),
            ('CompTIA Security+ Exam Prep', 'Network Security & Cryptography', 'Certification', 'Professor Messer', 'Beginner', '6 Weeks', 'Foundational cybersecurity principles.', 'https://www.professormesser.com', True),
            ('Figma UI/UX Design Essentials', 'Figma', 'Course', 'Skillshare', 'Beginner', '4 Weeks', 'UI/UX prototyping and wireframing.', 'https://www.figma.com', True)
        ]:
            if s_name in skill_map:
                LearningResource.objects.get_or_create(title=title, defaults={'skill': skill_map[s_name], 'category': cat, 'platform': plat, 'level': lvl, 'duration': dur, 'description': desc, 'resource_url': url, 'is_free': is_free, 'rating': 4.8})

        # 6. Projects
        for p_title, c_title, diff, desc, hours in [
            ('E-Commerce Analytics & Churn Predictor', 'Data Analyst', 'Intermediate', 'Interactive dashboard analyzing customer transactions and forecasting churn with SQL & Pandas.', 40),
            ('AI Disease Detection with Deep Learning', 'Machine Learning Engineer', 'Advanced', 'CNN classifier trained on medical imaging with FastAPI deployment.', 50),
            ('Real-Time Kanban Project Management App', 'Web Developer', 'Intermediate', 'Full stack React & Django portal with drag-and-drop tasks and user authentication.', 45),
            ('Automated Network Vulnerability Auditor', 'Cybersecurity Analyst', 'Intermediate', 'Python security script scanning open ports, SSL configurations, and known CVEs.', 35),
            ('Microservice Cloud Orchestration with K8s', 'DevOps Engineer', 'Advanced', 'Kubernetes cluster deployment with automated GitHub Actions CI/CD and Grafana.', 60),
            ('Enterprise Full Stack E-Commerce Platform', 'Software Developer', 'Intermediate', 'Scalable product catalog with payment processing, caching, and order microservice.', 50),
            ('Customer Insights BI & Sentiment Portal', 'Business Analyst', 'Intermediate', 'Power BI analytics dashboard linked with customer survey text mining.', 40),
            ('Autonomous Agentic Customer Support Chatbot', 'AI Engineer', 'Advanced', 'RAG pipeline powered by LLMs and vector database for instant enterprise Q&A.', 55)
        ]:
            if c_title in career_map:
                p, _ = ProjectIdea.objects.get_or_create(title=p_title, career=career_map[c_title], defaults={'difficulty': diff, 'summary': desc, 'description': desc, 'key_features': 'Modular design, tests, documentation.', 'deliverables': 'GitHub Repo and live deployment.', 'estimated_hours': hours})

        # 7. Mock Interview Questions
        for c_title, cat, diff, q_text, ref_ans, keys in [
            ('Software Developer', 'Technical', 'Medium', 'What is the difference between an Interface and an Abstract Class?', 'An abstract class can have instance variables and concrete method implementations; an interface defines a contract of method signatures and supports multiple inheritance.', 'abstract class, interface, multiple inheritance, state, contract'),
            ('Software Developer', 'Technical', 'Medium', 'How do you design a database schema for an e-commerce order system?', 'Use normalized tables for Users, Products, Orders, and OrderItems. Ensure foreign key constraints, indexes on user_id and created_at, and transactions for checkout consistency.', 'normalization, foreign keys, indexes, transactions, order items'),
            ('Data Scientist', 'Technical', 'Medium', 'Explain the difference between Overfitting and Underfitting, and how to prevent them.', 'Overfitting occurs when a model learns training noise and fails on unseen data (addressed via regularization, dropout, pruning). Underfitting occurs when a model is too simple to capture patterns (addressed by increasing complexity or adding features).', 'overfitting, underfitting, bias, variance, regularization, generalization'),
            ('Data Scientist', 'Technical', 'Medium', 'When would you use Precision over Recall as your primary evaluation metric?', 'Use Precision when the cost of False Positives is high (e.g., spam detection where important emails shouldn\'t be flagged). Use Recall when False Negatives are dangerous (e.g., medical cancer diagnosis where missing a disease is critical).', 'precision, recall, false positive, false negative, trade-off'),
            ('Web Developer', 'Technical', 'Easy', 'Explain the concept of the Virtual DOM in React.', 'The Virtual DOM is a lightweight in-memory representation of the real DOM. React computes differences (diffing algorithm) and batches updates efficiently to minimize expensive real DOM operations.', 'virtual dom, in-memory, diffing, reconciliation, batch updates, performance'),
            ('Web Developer', 'Technical', 'Medium', 'What are Cross-Origin Resource Sharing (CORS) and CSRF attacks, and how do you protect against them?', 'CORS regulates which origins can request resources from a web server via headers like Access-Control-Allow-Origin. CSRF tricks authenticated users into submitting unwanted actions, mitigated using CSRF tokens and SameSite cookie policies.', 'cors, csrf, headers, origin, tokens, samesite'),
            ('Cybersecurity Analyst', 'Technical', 'Medium', 'What is the difference between Symmetric and Asymmetric Encryption?', 'Symmetric encryption uses the same shared secret key for encryption and decryption (e.g., AES). Asymmetric encryption uses a public key for encryption and a private key for decryption (e.g., RSA), ideal for key exchange.', 'symmetric, asymmetric, secret key, public key, private key, aes, rsa'),
            ('DevOps Engineer', 'Technical', 'Medium', 'Explain the differences between Docker Containers and Virtual Machines.', 'Containers share the host operating system kernel and isolate processes at the user space level, making them lightweight and fast to start. Virtual Machines run a full guest OS on top of a hypervisor with dedicated hardware virtualization.', 'containers, virtual machines, hypervisor, kernel, lightweight, isolation'),
            (None, 'HR', 'Easy', 'Tell me about a time you handled a disagreement in a project team.', 'During our sprint planning, a teammate and I had conflicting database schema approaches. I proposed benchmarking both options with test datasets. The data clearly showed the optimized schema had lower latency, resolving the disagreement collaboratively.', 'disagreement, collaboration, communication, data-driven, resolution, outcome'),
            (None, 'HR', 'Easy', 'Where do you see yourself in 3 to 5 years in the software industry?', 'I see myself taking on high-ownership technical leadership, designing scalable architectures, mentoring junior developers, and contributing to core mission-critical systems.', 'growth, leadership, architecture, mentoring, technical excellence')
        ]:
            c = career_map.get(c_title) if c_title else None
            InterviewQuestion.objects.get_or_create(question_text=q_text, defaults={'career': c, 'category': cat, 'difficulty': diff, 'reference_answer': ref_ans, 'key_concepts': keys, 'evaluation_rubric': 'Clarity, correctness, and structured reasoning.'})
            
        self.stdout.write(self.style.SUCCESS('Successfully completed database seeding!'))
