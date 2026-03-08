// Configuration
const API_ENDPOINT = 'http://localhost:8000/api/bounty/live-stats/'; // Replace with prod URL when deployed
const FUNDING_GOAL = 20000; // $20,000 USD Minimum Goal

// DOM Elements
const elements = {
    progress: document.getElementById('funding-progress'),
    total: document.getElementById('total-raised'),
    firstPlace: document.getElementById('prize-first'),
    secondPlace: document.getElementById('prize-second'),
    thirdPlace: document.getElementById('prize-third'),
    lastUpdated: document.getElementById('last-updated')
};

// Formatter for currency
const formatUSD = (amount) => {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
    }).format(amount);
};

// Formatter for date
const formatDate = (isoString) => {
    if (!isoString) return 'Never';
    const date = new Date(isoString);
    return date.toLocaleString();
};

// Update the DOM with fetched data
const updateDashboard = (data) => {
    if (data.status !== 'success') {
        console.error('Failed to parse API data');
        return;
    }

    const totalCalculated = data.grand_total_usd || 0;
    
    // Calculate progress bar percentage (cap at 100%)
    let progressPercent = (totalCalculated / FUNDING_GOAL) * 100;
    progressPercent = progressPercent > 100 ? 100 : progressPercent;

    // Update DOM texts
    elements.total.textContent = formatUSD(totalCalculated);
    elements.firstPlace.textContent = formatUSD(data.prize_tiers.first_place);
    elements.secondPlace.textContent = formatUSD(data.prize_tiers.second_place);
    elements.thirdPlace.textContent = formatUSD(data.prize_tiers.third_place);
    
    // Determine glow status based on funding success
    if (totalCalculated >= FUNDING_GOAL) {
        elements.progress.style.boxShadow = '0 0 20px #00ff88';
        elements.progress.style.background = '#00ff88';
    } else {
        elements.progress.style.boxShadow = '0 0 15px #00eaff';
        elements.progress.style.background = '#00eaff';
    }

    // Set width (triggers CSS transition)
    setTimeout(() => {
        elements.progress.style.width = `${progressPercent}%`;
    }, 100);

    elements.lastUpdated.textContent = formatDate(data.last_updated);
};

// Main fetch function
const fetchLiveStats = async () => {
    try {
        const response = await fetch(API_ENDPOINT);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        updateDashboard(data);
    } catch (error) {
        console.error('Error fetching bounty stats:', error);
        
        // Fallback demo values if the backend is down locally
        const demoData = {
            status: 'success',
            grand_total_usd: 12540.00,
            prize_tiers: {
                first_place: 7524.00,
                second_place: 2508.00,
                third_place: 1254.00,
                vip_pool: 627.00,
                admin_award: 627.00
            },
            last_updated: new Date().toISOString()
        };
        console.log("Serving demo data for UI testing since backend is unreachable.");
        updateDashboard(demoData);
    }
};

// Initial Fetch
fetchLiveStats();

// Poll every 30 seconds
setInterval(fetchLiveStats, 30000);
