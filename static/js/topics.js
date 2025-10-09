// English Communication Course Topics
// Edit this file to add new topics or modify existing ones

const topics = [
    {
        id: 'business_communication',
        title: 'Business Communication',
        description: 'Professional communication skills for workplace environments',
        icon: 'fas fa-briefcase',
        temperature: 0.7,
        estimatedTime: '15-20 min',
        prompt: `Create comprehensive business communication content focusing on:

1. Professional email writing
2. Meeting communication etiquette
3. Presentation skills
4. Workplace conversations
5. Negotiation language

Include practical examples and scenarios that students can relate to. Make the content interactive and engaging for adult learners in a corporate environment.

Focus on:
- Formal vs informal communication
- Key phrases and expressions
- Common mistakes to avoid
- Cultural considerations
- Digital communication best practices`
    },
    {
        id: 'conversation_skills',
        title: 'Conversation Skills',
        description: 'Everyday conversation practice and social interaction skills',
        icon: 'fas fa-comments',
        temperature: 0.8,
        estimatedTime: '10-15 min',
        prompt: `Generate engaging conversation skills content covering:

1. Starting and maintaining conversations
2. Small talk topics and techniques
3. Active listening skills
4. Non-verbal communication
5. Handling awkward silences

Create realistic dialogue examples and practice scenarios. Include:
- Conversation starters for different situations
- Cultural dos and don'ts
- Body language awareness
- Empathy and emotional intelligence
- Recovery from communication breakdowns

Make the content suitable for intermediate to advanced English learners.`
    },
    {
        id: 'pronunciation_practice',
        title: 'Pronunciation & Phonetics',
        description: 'Sound production, stress patterns, and accent reduction',
        icon: 'fas fa-volume-up',
        temperature: 0.6,
        estimatedTime: '20-25 min',
        prompt: `Create pronunciation and phonetics content including:

1. Common pronunciation challenges
2. Word stress patterns
3. Sentence rhythm and intonation
4. Vowel and consonant sounds
5. Linking and connected speech

Provide:
- Minimal pair exercises
- Stress pattern practice words
- Intonation patterns for different sentence types
- Common pronunciation errors and corrections
- Practice tongue twisters and phrases

Focus on the most challenging sounds for non-native speakers and include phonetic symbols where helpful.`
    },
    {
        id: 'grammar_practice',
        title: 'Grammar in Context',
        description: 'Practical grammar application in real communication',
        icon: 'fas fa-spell-check',
        temperature: 0.5,
        estimatedTime: '15-20 min',
        prompt: `Develop contextual grammar content focusing on:

1. Common grammar mistakes in spoken English
2. Tense usage in natural conversation
3. Modal verbs for different situations
4. Conditional sentences in practice
5. Reported speech in everyday use

Create:
- Real-world examples and contexts
- Error correction exercises
- Grammar rules in communicative situations
- Practice with natural language patterns
- Common collocations and phrasal verbs

Emphasize grammar as a tool for better communication rather than abstract rules.`
    },
    {
        id: 'presentation_skills',
        title: 'Presentation Skills',
        description: 'Public speaking and presentation techniques',
        icon: 'fas fa-chalkboard-teacher',
        temperature: 0.7,
        estimatedTime: '25-30 min',
        prompt: `Create comprehensive presentation skills content covering:

1. Structuring effective presentations
2. Opening and closing techniques
3. Visual aid integration
4. Audience engagement strategies
5. Handling questions and feedback

Include:
- Presentation language and phrases
- Body language and stage presence
- Voice modulation and pace
- Dealing with nervousness
- Technology integration tips
- Cultural considerations for international audiences

Provide practical exercises and evaluation criteria for self-assessment.`
    },
    {
        id: 'listening_comprehension',
        title: 'Listening Comprehension',
        description: 'Advanced listening skills for various contexts',
        icon: 'fas fa-ear-listen',
        temperature: 0.6,
        estimatedTime: '20-25 min',
        prompt: `Develop listening comprehension content featuring:

1. Different accents and speaking speeds
2. Context clues and inference skills
3. Note-taking strategies
4. Listening for specific information
5. Understanding implied meaning

Create content for:
- Academic lectures and presentations
- Business meetings and conferences
- Casual conversations and discussions
- Phone conversations and voicemails
- News broadcasts and interviews

Include strategies for improving listening skills and overcoming common challenges.`
    },
    {
        id: 'writing_skills',
        title: 'Writing Skills',
        description: 'Written communication for various purposes and audiences',
        icon: 'fas fa-pen-fancy',
        temperature: 0.6,
        estimatedTime: '20-25 min',
        prompt: `Generate writing skills content covering:

1. Different writing styles and purposes
2. Email and digital communication
3. Report and proposal writing
4. Creative and descriptive writing
5. Editing and proofreading techniques

Include:
- Structure and organization principles
- Tone and audience awareness
- Grammar and style consistency
- Cohesion and coherence
- Common writing errors and solutions

Provide templates and examples for different types of writing tasks.`
    },
    {
        id: 'cultural_communication',
        title: 'Cultural Communication',
        description: 'Cross-cultural awareness and international communication',
        icon: 'fas fa-globe',
        temperature: 0.8,
        estimatedTime: '15-20 min',
        prompt: `Create cultural communication content addressing:

1. Cultural differences in communication styles
2. Non-verbal communication across cultures
3. Politeness and formality levels
4. Conflict resolution in multicultural settings
5. Building rapport across cultures

Cover:
- High-context vs low-context cultures
- Direct vs indirect communication styles
- Cultural taboos and sensitive topics
- International business etiquette
- Adapting communication style to audience

Provide real-world scenarios and cultural insights for global communication.`
    }
];

// Make topics available globally
window.topics = topics;
