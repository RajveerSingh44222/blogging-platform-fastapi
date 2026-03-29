const defaultPosts = [
  {
    id: 1,
    cat: 'design',
    tag: 'Design',
    title: 'The invisible hand: how great UX disappears into the product',
    excerpt: 'When design works, nobody notices it. That invisibility is the hardest thing to build.',
    content: 'When design works, it steps out of the spotlight and lets the user move freely. Great UX removes friction, reduces doubt, and makes the product feel obvious.\n\nThis article explores why invisible design is often the hardest kind to create. It requires clarity, restraint, and a deep understanding of user behaviour.\n\nThe best designers are not the ones who add the most elements. They are the ones who know what to leave out.',
    author: 'Arjun Kumar',
    initials: 'AK',
    publishDate: '2026-03-21',
    read: '6 min',
    likes: 2400,
    comments: 118,
    letter: 'A'
  },
  {
    id: 2,
    cat: 'tech',
    tag: 'Tech',
    title: 'FastAPI vs Django: what I learned building a production API',
    excerpt: 'After shipping three projects with each framework, here\'s what actually matters at scale.',
    content: 'FastAPI feels incredibly productive when you want speed, automatic docs, and modern Python typing. Django feels complete when the project needs a mature admin, batteries-included architecture, and fast business workflows.\n\nThis comparison focuses on practical tradeoffs: performance, learning curve, validation, ORM experience, and scaling decisions.',
    author: 'Priya Sharma',
    initials: 'PS',
    publishDate: '2026-03-22',
    read: '9 min',
    likes: 1800,
    comments: 76,
    letter: 'F'
  },
  {
    id: 3,
    cat: 'culture',
    tag: 'Culture',
    title: 'The loneliness of the deep work era',
    excerpt: 'We optimised for focus and got isolation. Was it worth it?',
    content: 'Deep work gave many people a way to protect their attention. But somewhere along the way, solitude started becoming the default mode of work.\n\nThis piece reflects on what productivity culture gave us, and what it quietly took away in terms of community, collaboration, and emotional energy.',
    author: 'Rahul Mehta',
    initials: 'RM',
    publishDate: '2026-03-23',
    read: '5 min',
    likes: 3100,
    comments: 143,
    letter: 'L'
  },
  {
    id: 4,
    cat: 'design',
    tag: 'Design',
    title: 'Dark mode is not just a preference — it\'s a philosophy',
    excerpt: 'How the choice of a colour scheme reflects everything about your relationship with your users.',
    content: 'Dark mode is often treated like a visual setting, but it says much more about comfort, accessibility, identity, and product tone.\n\nIn this article, we look at why dark interfaces feel premium, when they improve usability, and when they become design theatre.',
    author: 'Neha Joshi',
    initials: 'NJ',
    publishDate: '2026-03-24',
    read: '7 min',
    likes: 980,
    comments: 39,
    letter: 'D'
  },
  {
    id: 5,
    cat: 'tech',
    tag: 'Tech',
    title: 'MySQL indexing strategies that actually made a difference',
    excerpt: 'Theory is nice. Here are the five index patterns that cut our query time by 80%.',
    content: 'Indexes become meaningful only when they match actual query patterns. This write-up explains how composite indexes, covering indexes, and selective indexing improved performance in production.\n\nThe goal is not more indexes. The goal is smarter indexes.',
    author: 'Karan Patel',
    initials: 'KP',
    publishDate: '2026-03-25',
    read: '11 min',
    likes: 1250,
    comments: 52,
    letter: 'M'
  },
  {
    id: 6,
    cat: 'culture',
    tag: 'Culture',
    title: 'Why I deleted my recommendation feeds and what happened next',
    excerpt: 'Three months without algorithmic content. A personal account.',
    content: 'Without endless recommendations, the internet felt quieter. It also felt slower, emptier, and strangely more intentional.\n\nThis is a reflection on attention, habit, and what happens when discovery becomes a manual act again.',
    author: 'Sanya Roy',
    initials: 'SR',
    publishDate: '2026-03-26',
    read: '4 min',
    likes: 4700,
    comments: 201,
    letter: 'W'
  }
];

const trendingData = [
  { tag: 'Tech', title: 'JWT authentication from scratch in Python', meta: '14.2k reads' },
  { tag: 'Design', title: 'Colour theory for developers who can\'t design', meta: '9.8k reads' },
  { tag: 'Culture', title: 'The second brain hype is over. Now what?', meta: '7.1k reads' },
  { tag: 'Tech', title: 'React state management in 2025', meta: '6.4k reads' }
];

const tagsData = ['javascript', 'python', 'fastapi', 'react', 'ux', 'writing', 'productivity', 'css', 'mysql', 'startup', 'design', 'philosophy'];
