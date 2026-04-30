const { createApp } = Vue;

createApp({
  data() {
    return {
      menuOpen: false,
      activeTab: 'All',
      email: '',
      subscribed: false,
      contactSent: false,
      contact: { name: '', email: '', service: '', message: '' },

      navLinks: [
        { label: 'Home',      href: 'index.html' },
        { label: 'About',     href: 'about.html' },
        { label: 'Services',  href: 'services.html' },
        { label: 'Our Work',  href: 'portfolio.html' },
        { label: 'Contact',   href: 'index.html#contact' },
      ],

      services: [
        {
          icon: '✦',
          title: 'Brand Identity Design',
          desc: 'Logos, colour systems, typography, and full brand guidelines that make your business instantly recognisable.',
          tags: ['Logo Design', 'Brand Guidelines', 'Rebranding'],
          image: 'https://images.unsplash.com/photo-1626785774573-4b799315345d?w=900&auto=format&fit=crop&q=80',
        },
        {
          icon: '⬡',
          title: 'Web Design & Development',
          desc: 'Modern, fast, responsive websites built with performance and conversion in mind. Laravel, Tailwind, and more.',
          tags: ['UI/UX', 'Laravel', 'E-commerce'],
          image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=900&auto=format&fit=crop&q=80',
        },
        {
          icon: '◈',
          title: 'Event Branding',
          desc: 'Immersive event experiences — from stage concepts and backdrops to digital graphics and sponsorship packages.',
          tags: ['Event Logos', 'Signage', 'Digital Graphics'],
          image: 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=900&auto=format&fit=crop&q=80',
        },
        {
          icon: '◉',
          title: 'Social Media Management',
          desc: 'Strategy, content, branded graphics, reels, ads management, and monthly analytics — all handled for you.',
          tags: ['Strategy', 'Content', 'Ads'],
          image: 'https://images.unsplash.com/photo-1611162616305-69e3e44047a6?w=900&auto=format&fit=crop&q=80',
        },
        {
          icon: '▣',
          title: 'Motion Graphics & Video',
          desc: 'Corporate videos, animated explainers, social reels, and cinematic event coverage that move audiences.',
          tags: ['Animation', 'Corporate Video', 'Reels'],
          image: 'https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=900&auto=format&fit=crop&q=80',
        },
        {
          icon: '⬘',
          title: 'Print & Digital Marketing',
          desc: 'Flyers, brochures, packaging, and targeted digital ad campaigns that work together to grow your brand.',
          tags: ['Print Design', 'Ads', 'Packaging'],
          image: 'https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=900&auto=format&fit=crop&q=80',
        },
        {
          icon: '◌',
          title: 'Photography & Videography',
          desc: 'Professional event coverage, product photography, and corporate shoots that tell your story visually.',
          tags: ['Events', 'Products', 'Corporate'],
          image: 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=900&auto=format&fit=crop&q=80',
        },
        {
          icon: '❖',
          title: 'Consulting & Strategy',
          desc: 'Expert brand positioning, digital transformation guidance, and integrated creative direction for growth.',
          tags: ['Strategy', 'Digital', 'Creative Direction'],
          image: 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=900&auto=format&fit=crop&q=80',
        },
        {
          icon: '◭',
          title: 'Consulting & Integrated Solutions',
          desc: 'We guide businesses through positioning, communication strategy, and full creative ecosystem builds.',
          tags: ['Consulting', 'Positioning', 'Integration'],
          image: 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=900&auto=format&fit=crop&q=80',
        },
      ],

      process: [
        { title: 'Discovery', desc: 'Deep-dive into your brand, goals, and audience through research and consultation.' },
        { title: 'Design', desc: 'Translating insights into compelling visual concepts aligned with your identity.' },
        { title: 'Development', desc: 'Bringing designs to life — responsive, functional, and meticulously crafted.' },
        { title: 'Launch & Support', desc: 'Flawless delivery and post-launch guidance to maximise your new presence.' },
      ],

      portfolioTabs: ['All', 'Branding', 'Web Design', 'Events', 'Print'],

      portfolio: [
        { title: 'Magnox Investments', year: '2024', categories: ['Branding'], image: 'https://images.unsplash.com/photo-1626785774573-4b799315345d?w=1200&auto=format&fit=crop&q=80' },
        { title: 'Zenith Corporate Identity', year: '2024', categories: ['Branding', 'Print'], image: 'https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=1200&auto=format&fit=crop&q=80' },
        { title: 'Africast Media Site', year: '2024', categories: ['Web Design'], image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200&auto=format&fit=crop&q=80' },
        { title: 'ZDA Event Branding', year: '2023', categories: ['Events'], image: 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1200&auto=format&fit=crop&q=80' },
        { title: 'Ecobank Zambia Campaign', year: '2023', categories: ['Branding', 'Print'], image: 'https://images.unsplash.com/photo-1486406146926-c627a92ad188?w=1200&auto=format&fit=crop&q=80' },
      ],

      stats: [
        { value: '7+',   label: 'Years of Experience',  sub: 'In the creative industry' },
        { value: '100+', label: 'Projects Delivered',   sub: 'Across all service areas' },
        { value: '98%',  label: 'Client Satisfaction',  sub: 'Long-term partnerships' },
        { value: '13+',  label: 'Active Clients',       sub: 'Zambia & beyond' },
      ],

      clients: ['FC Bwacha', 'Skin Sensation', 'Zenith', 'Access Bank', 'Africast', 'ZDA', 'Amiran', 'Ecobank', 'Mannock', 'Lukanda', 'Ntumai', 'Freedom'],

      testimonials: [
        {
          quote: "Working with Kinpin Arts was a game-changer for our online presence. The new website exceeded our expectations in both design and functionality. Absolutely world-class.",
          name: 'Jerome Bell', title: 'CTO, Waverio', initials: 'JB',
        },
        {
          quote: "Kinpin Arts delivered a stunning brand identity that truly reflects our essence. Their attention to detail, responsiveness, and creative vision are second to none. Highly recommended.",
          name: 'Wade Warren', title: 'Founder, Creaty', initials: 'WW',
        },
      ],

      socials: [
        { name: 'Be', icon: 'Be', href: 'https://www.behance.net/KinpinArts' },
        { name: 'IG', icon: 'IG', href: '#' },
        { name: 'LI', icon: 'in', href: '#' },
        { name: 'X',  icon: 'X',  href: '#' },
      ],
    };
  },

  computed: {
    filteredPortfolio() {
      if (this.activeTab === 'All') return this.portfolio;
      return this.portfolio.filter(p => p.categories.includes(this.activeTab));
    },
  },

  methods: {
    subscribeNewsletter() {
      this.subscribed = true;
      this.email = '';
    },
    submitContact() {
      this.contactSent = true;
      this.contact = { name: '', email: '', service: '', message: '' };
    },
    initScrollReveal() {
      const els = document.querySelectorAll('.reveal');
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(e => {
          if (e.isIntersecting) {
            e.target.classList.add('visible');
            observer.unobserve(e.target);
          }
        });
      }, { threshold: 0.12 });
      els.forEach(el => observer.observe(el));
    },
  },

  mounted() {
    this.$nextTick(() => this.initScrollReveal());
  },
}).mount('#app');
