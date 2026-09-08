# -*- coding: utf-8 -*-
import re
from careers.models import Career, Skill, CareerSkill
from students.models import StudentSkill
from skill_gap.services import calculate_skill_gap

RESPONSES_I18N = {
    "greeting": {
        "en": "Hi {name}! 😊 I am **CareerMate**, your friendly AI career companion.\n\nI can help you:\n- Find the best career path for you\n- Identify missing skills & learning roadmaps\n- Analyze your resume & get ATS tips\n- Recommend cool portfolio projects\n- Practice mock interview questions\n\nWhat are you curious about today?",
        "te": "నమస్కారం {name}! 😊 నేను మీ **CareerMate** - స్నేహపూర్వక AI కెరీర్ గైడ్.\n\nనేను మీకు సహాయం చేయగలను:\n- మీకు సరిపోయే ఉత్తమ కెరీర్ మార్గాన్ని కనుగొనడం\n- మీరు నేర్చుకోవాల్సిన స్కిల్స్ & రోడ్‌మ్యాప్\n- మీ రెజ్యూమ్‌ను విశ్లేషించడం & మెరుగుపరచడం\n- ప్రాజెక్ట్ ఐడియాలు & ఇంటర్వ్యూ ప్రిపరేషన్\n\nమీరు ఈరోజు దేని గురించి తెలుసుకోవాలనుకుంటున్నారు?",
        "hi": "नमस्ते {name}! 😊 मैं आपका **CareerMate** - AI करियर साथी हूँ।\n\nमैं आपकी मदद कर सकता हूँ:\n- आपके लिए सही करियर विकल्प चुनने में\n- छूटे हुए स्किल्स और लर्निंग रोडमैप जानने में\n- अपने रेज़्यूमे का विश्लेषण करने में\n- प्रोजेक्ट्स और इंटरव्यू की तैयारी में\n\nआज आप किस बारे में पूछना चाहते हैं?"
    },
    "career_guidance": {
        "en": "Based on your academic profile and skill ratings, here are your top career recommendations:\n\n{recs}\n\n🌟 **My Advice**: You have great potential for **{top_career}**! Want me to show your skill gaps or a step-by-step roadmap?",
        "te": "మీ అకడమిక్ ప్రొఫైల్ మరియు స్కిల్ రేటింగ్స్ ఆధారంగా మీ టాప్ కెరీర్ సిఫార్సులు ఇక్కడ ఉన్నాయి:\n\n{recs}\n\n🌟 **నా సలహా**: మీకు **{top_career}** కి మంచి అనుకూలత ఉంది! మీ స్కిల్ గ్యాప్స్ లేదా రోడ్‌మ్యాప్ చూడాలనుకుంటున్నారా?",
        "hi": "आपकी प्रोफाइल और स्किल्स के आधार पर आपकी टॉप करियर सिफारिशें ये हैं:\n\n{recs}\n\n🌟 **मेरी सलाह**: आप **{top_career}** के लिए बहुत उपयुक्त हैं! क्या आप इसके स्किल गैप्स या रोडमैप देखना चाहते हैं?"
    },
    "skill_gap": {
        "en": "📊 **Skill Analysis for {career}** (Readiness: {readiness}%):\n\n- ✅ **Strong Skills**: {strong}\n- ⚠️ **Skills to Improve**: {moderate}\n- ❌ **Missing Skills**: {missing}\n\n💡 **Next Step**: Focus on mastering {top_missing} first.",
        "te": "📊 **{career} కోసం స్కిల్ విశ్లేషణ** (సంసిద్ధత: {readiness}%):\n\n- ✅ **బలమైన స్కిల్స్**: {strong}\n- ⚠️ **మెరుగుపరచుకోవాల్సినవి**: {moderate}\n- ❌ **నేర్చుకోవాల్సిన ముఖ్యమైనవి**: {missing}\n\n💡 **ముఖ్యమైన సలహా**: ముందుగా {top_missing} పై దృష్టి పెట్టండి.",
        "hi": "📊 **{career} के लिए स्किल एनालिसिस** (तैयारी: {readiness}%):\n\n- ✅ **मजबूत स्किल्स**: {strong}\n- ⚠️ **सुधारने योग्य स्किल्स**: {moderate}\n- ❌ **सीखने योग्य मुख्य स्किल्स**: {missing}\n\n💡 **सुझाव**: सबसे पहले {top_missing} सीखने पर ध्यान दें।"
    },
    "roadmap": {
        "en": "🚀 **Learning Roadmap for {career}**:\n\n1. **Step 1: Core Fundamentals** - Master language syntax, DSA, and Git.\n2. **Step 2: Frameworks & Databases** - Build database schemas & REST APIs.\n3. **Step 3: Practical Projects** - Create 2-3 real-world portfolio applications.\n4. **Step 4: Deployment & Tools** - Learn Docker & cloud basics.\n5. **Step 5: Interview Prep** - Practice coding problems & mock interviews.\n\nYou can track each milestone directly in your **Learning Roadmap** tab! 🎯",
        "te": "🚀 **{career} కోసం లెర్నింగ్ రోడ్‌మ్యాప్**:\n\n1. **దశ 1: ఫండమెంటల్స్** - ప్రోగ్రామింగ్, డేటా స్ట్రక్చర్స్, Git.\n2. **దశ 2: ఫ్రేమ్‌వర్క్స్ & డేటాబేస్** - SQL, REST APIs, బ్యాకెండ్.\n3. **దశ 3: ప్రాజెక్టులు** - 2-3 ప్రాక్టికల్ పోర్ట్‌ఫోలియో ప్రాజెక్ట్‌లు నిర్మించండి.\n4. **దశ 4: డిప్లాయ్‌మెంట్** - Docker మరియు క్లౌడ్ బేసిక్స్.\n5. **దశ 5: ఇంటర్వ్యూ సాధన** - మాక్ ఇంటర్వ్యూలు & కోడింగ్ ప్రశ్నలు.\n\nమీరు మీ **రోడ్‌మ్యాప్** పేజీలో పురోగతిని ట్రాక్ చేయవచ్చు! 🎯",
        "hi": "🚀 **{career} के लिए लर्निंग रोडमैप**:\n\n1. **चरण 1: बेसिक्स** - प्रोग्रामिंग, डेटा स्ट्रक्चर्स और Git.\n2. **चरण 2: फ्रेमवर्क्स और डेटाबेस** - SQL, REST APIs और बैकएंड.\n3. **चरण 3: प्रोजेक्ट्स** - 2-3 रियल-वर्ल्ड प्रोजेक्ट्स बनाएं।\n4. **चरण 4: डिप्लॉयमेंट** - Docker और क्लाउड बेसिक्स सीखें।\n5. **चरण 5: इंटरव्यू तैयारी** - मॉक इंटरव्यू और कोडिंग प्रैक्टिस करें।\n\nआप अपने **लर्निंग रोडमैप** पेज में प्रगति ट्रैक कर सकते हैं! 🎯"
    },
    "projects": {
        "en": "💡 **Recommended Projects for {career}**:\n\n- **Beginner**: Student Management Portal (CRUD, Database, Clean UI)\n- **Intermediate**: E-Commerce / Job Portal with Auth & REST API\n- **Advanced**: Real-Time AI / Cloud Microservice with Docker\n\nCheck out the **Projects** tab for step-by-step deliverable guides! 🚀",
        "te": "💡 **{career} కోసం సిఫార్సు చేయబడిన ప్రాజెక్టులు**:\n\n- **ప్రారంభ స్థాయి**: స్టూడెంట్ మేనేజ్‌మెంట్ పోర్టల్ (CRUD, SQL, UI)\n- **మధ్యస్థ స్థాయి**: జాబ్ పోర్టల్ / ఈ-కామర్స్ వెబ్‌సైట్ (REST APIs)\n- **అడ్వాన్స్‌డ్**: రియల్-టైమ్ AI లేదా మైక్రోసర్వీస్ ప్రాజెక్ట్ (Docker)\n\nపూర్తి వివరాల కోసం **Projects** ట్యాబ్ చూడండి! 🚀",
        "hi": "💡 **{career} के लिए प्रोजेक्ट आइडियाज**:\n\n- **शुरुआती**: स्टूडेंट मैनेजमेंट सिस्टम (CRUD, SQL, UI)\n- **मध्यम**: ई-कॉमर्स / जॉब पोर्टल (Auth & REST APIs)\n- **एडवांस्ड**: रियल-टाइम AI या क्लाउड माइक्रोसर्विस (Docker)\n\nअधिक जानकारी के लिए **Projects** टैब देखें! 🚀"
    },
    "resume_tips": {
        "en": "📄 **CareerMate Resume Tips**:\n\n1. **Use Action Verbs**: Start bullets with words like *Developed, Engineered, Optimized, Designed*.\n2. **Quantify Results**: Write *Reduced load time by 40%* instead of just *Worked on website*.\n3. **Include Key Sections**: Contact info, Education, Technical Skills, Projects, and Certifications.\n4. **ATS Check**: Upload your resume to our **Resume Analyzer** tab to get your instant score! ✨",
        "te": "📄 **కెరీర్‌మేట్ రెజ్యూమ్ చిట్కాలు**:\n\n1. **యాక్షన్ వెర్బ్స్ వాడండి**: *Developed, Built, Optimized* వంటి పదాలతో ప్రారంభించండి.\n2. **ఫలితాలను నంబర్లలో చూపించండి**: ఉదాహరణకు *Reduced response time by 40%*.\n3. **ముఖ్యమైన విభాగాలు**: విద్య, టెక్నికల్ స్కిల్స్, ప్రాజెక్ట్‌లు, సర్టిఫికేషన్లు.\n4. **ATS స్కోర్ చెక్**: పూర్తి విశ్లేషణ కోసం **Resume Analyzer** లో అప్‌లోడ్ చేయండి! ✨",
        "hi": "📄 **करियरमेट रेज़्यूमे टिप्स**:\n\n1. **एक्शन वर्ब्स का उपयोग करें**: *Developed, Designed, Optimized* जैसे शब्दों से शुरू करें।\n2. **रिजल्ट्स को नंबर्स में बताएं**: जैसे *API स्पीड 40% तेज की*।\n3. **महत्वपूर्ण सेक्शन्स शामिल करें**: एजुकेशन, टेक्निकल स्किल्स, प्रोजेक्ट्स और सर्टिफिकेशन।\n4. **ATS स्कोर**: तुरंत स्कोर जानने के लिए **Resume Analyzer** में रेज़्यूमे अपलोड करें! ✨"
    },
    "interview_tips": {
        "en": "🎯 **Mock Interview Tips**:\n\n1. **STAR Method**: For behavioral questions, explain the Situation, Task, Action, and Result.\n2. **Explain Complexity**: Always state Time & Space Big-O complexity for data structures.\n3. **Practice Out Loud**: Head over to our **Mock Interview** tab to test your answers with real-time NLP semantic scoring! 🎤",
        "te": "🎯 **మాక్ ఇంటర్వ్యూ చిట్కాలు**:\n\n1. **STAR పద్ధతి**: Situation, Task, Action, Result రూపంలో సమాధానం చెప్పండి.\n2. **కాంప్లెక్సిటీ వివరించండి**: ఆల్గోరిథమ్స్ కి Time & Space complexity స్పష్టంగా చెప్పండి.\n3. **సాధన చేయండి**: మా **Mock Interview** ట్యాబ్ లో ప్రాక్టీస్ చేసి తక్షణ NLP స్కోర్ పొందండి! 🎤",
        "hi": "🎯 **मॉक इंटरव्यू टिप्स**:\n\n1. **STAR मेथड**: सिचुएशन, टास्क, एक्शन और रिजल्ट के साथ उत्तर दें।\n2. **टाइम कॉम्प्लेक्सिटी बताएं**: कोडिंग सवालों में Time & Space complexity स्पष्ट करें।\n3. **प्रैक्टिस करें**: रियल-टाइम NLP स्कोरिंग के लिए **Mock Interview** सेक्शन में अभ्यास करें! 🎤"
    },
    "fallback": {
        "en": "That is a great question about **{query}**! 😊 As your career buddy, I recommend exploring your skill proficiencies, checking your personalized roadmap, or practicing a quick mock interview. What would you like to explore next?",
        "te": "**{query}** గురించి మంచి ప్రశ్న అడిగారు! 😊 మీ కెరీర్ స్నేహితుడిగా, మీ స్కిల్ గ్యాప్స్ చెక్ చేయడం, రోడ్‌మ్యాప్ చూడటం లేదా మాక్ ఇంటర్వ్యూ సాధన చేయాలని సూచిస్తున్నాను. తర్వాత ఏం చేయాలనుకుంటున్నారు?",
        "hi": "**{query}** के बारे में बढ़िया सवाल है! 😊 आपके करियर गाइड के रूप में, मैं आपकी स्किल्स चेक करने, लर्निंग रोडमैप देखने या मॉक इंटरव्यू का अभ्यास करने की सलाह देता हूँ। आगे क्या जानना चाहते हैं?"
    }
}

CHIPS_I18N = {
    "en": ["What career suits me?", "What skills am I missing?", "Show learning roadmap", "Recommend a project", "Resume tips", "Mock interview"],
    "te": ["నాకు ఏ కెరీర్ బాగుంటుంది?", "నేను ఏ స్కిల్స్ నేర్చుకోవాలి?", "లెర్నింగ్ రోడ్‌మ్యాప్", "ప్రాజెక్ట్ సిఫార్సులు", "రెజ్యూమ్ చిట్కాలు", "మాక్ ఇంటర్వ్యూ"],
    "hi": ["मेरे लिए कौन सा करियर सही है?", "मुझे कौन से स्किल्स सीखने चाहिए?", "लर्निंग रोडमैप", "प्रोजेक्ट आइडियाज", "रेज़्यूमे टिप्स", "मॉक इंटरव्यू"]
}

def generate_bot_response(user_message, student_profile=None, lang="en"):
    msg = user_message.lower().strip()
    lang = lang if lang in ["en", "te", "hi"] else "en"
    
    student_name = student_profile.user.first_name if student_profile and student_profile.user.first_name else ("Student" if lang=="en" else ("మిత్రమా" if lang=="te" else "दोस्त"))
    target_career = student_profile.target_career if student_profile else None
    target_title = target_career.title if target_career else "Software Developer"
    
    chips = CHIPS_I18N[lang]
    
    if re.search(r"\b(hello|hi|hey|greetings|morning|evening|namaste|namaskaram|హలో|నమస్కారం|नमस्ते|హాయ్)\b", msg):
        text = RESPONSES_I18N["greeting"][lang].format(name=student_name)
        return text, chips

    if re.search(r"\b(career|suitable|recommend|role|job|choice|what should i do|career for me|career suits|కెరీర్|ఉద్యోగం|करियर|नौकरी|विकल्प)\b", msg):
        if student_profile:
            rec_logs = student_profile.recommendation_logs.all()[:3]
            if rec_logs:
                recs_lines = [f"**{i+1}. {r.career.title}** - {r.suitability_score}% Match ({'High Match' if r.suitability_score>=85 else 'Good Match'})" for i, r in enumerate(rec_logs)]
                recs_str = "\n".join(recs_lines)
                top_c = rec_logs[0].career.title
            else:
                recs_str = f"**1. {target_title}** (Top Choice)\n**2. Data Analyst** (Good Match)\n**3. Web Developer** (Good Match)"
                top_c = target_title
        else:
            recs_str = "**1. Software Developer**\n**2. Data Analyst**\n**3. Web Developer**"
            top_c = "Software Developer"
            
        text = RESPONSES_I18N["career_guidance"][lang].format(recs=recs_str, top_career=top_c)
        return text, chips

    if re.search(r"\b(skill|missing|gap|improve|learn next|what to learn|after python|స్కిల్స్|నైపుణ్యాలు|స్కిల్|स्किल्स|कमी|क्या सीखूं)\b", msg):
        active_career = target_career or Career.objects.first()
        if student_profile and active_career:
            gap_data = calculate_skill_gap(student_profile, active_career)
            missing = [g['name'] for g in gap_data['skill_gaps']]
            moderate = [m['name'] for m in gap_data['moderate_skills']]
            strong = [s['name'] for s in gap_data['strong_skills']]
            
            missing_str = ", ".join(missing[:4]) if missing else ("None! You have great coverage" if lang=="en" else "అన్నీ కవర్ అయ్యాయి!")
            moderate_str = ", ".join(moderate[:4]) if moderate else ("None" if lang=="en" else "ఏమీ లేవు")
            strong_str = ", ".join(strong[:4]) if strong else ("Keep building initial skills" if lang=="en" else "బేసిక్స్ ప్రాక్టీస్ చేయండి")
            top_missing = missing[0] if missing else ("advanced topics" if lang=="en" else "అడ్వాన్స్‌డ్ కాన్సెప్ట్స్")
            
            text = RESPONSES_I18N["skill_gap"][lang].format(
                career=active_career.title,
                readiness=gap_data['readiness_percentage'],
                strong=strong_str,
                moderate=moderate_str,
                missing=missing_str,
                top_missing=top_missing
            )
        else:
            text = RESPONSES_I18N["skill_gap"][lang].format(
                career=target_title,
                readiness=70,
                strong="Python, SQL, HTML",
                moderate="Data Structures, REST APIs",
                missing="Docker, Cloud Deployment, Git",
                top_missing="Data Structures & Git"
            )
        return text, chips

    if re.search(r"\b(roadmap|path|steps|guide|stage|రోడ్‌మ్యాప్|మార్గం|रोडमॅप|रास्ता|कदम)\b", msg):
        active_career = target_career.title if target_career else "Software Developer"
        text = RESPONSES_I18N["roadmap"][lang].format(career=active_career)
        return text, chips

    if re.search(r"\b(project|projects|build|portfolio|capstone|ప్రాజెక్ట్|ప్రాజెక్టులు|प्रोजेक्ट)\b", msg):
        active_career = target_career.title if target_career else "Software Developer"
        text = RESPONSES_I18N["projects"][lang].format(career=active_career)
        return text, chips

    if re.search(r"\b(resume|cv|ats|format|bio|రెజ్యూమ్|रेज़्यूमे|बायोडाटा)\b", msg):
        text = RESPONSES_I18N["resume_tips"][lang]
        return text, chips

    if re.search(r"\b(interview|prepare|questions|tips|star|ఇంటర్వ్యూ|ఇంటర్వ్యూలు|इंटरव्यू)\b", msg):
        text = RESPONSES_I18N["interview_tips"][lang]
        return text, chips

    clean_q = user_message[:40]
    text = RESPONSES_I18N["fallback"][lang].format(query=clean_q)
    return text, chips
