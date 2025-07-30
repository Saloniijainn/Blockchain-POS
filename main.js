// DOM Elements
const nodeInput = document.getElementById('node');
const amountInput = document.getElementById('amt');
const chainDisplay = document.getElementById('chain');
const mineStatus = document.getElementById('mine-status');

// Display status message
function showStatus(message, isError = false) {
    const statusDiv = document.createElement('div');
    statusDiv.textContent = message;
    statusDiv.className = isError ? 'status error' : 'status success';
    document.body.appendChild(statusDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => statusDiv.remove(), 5000);
}

// Stake tokens function
async function stake() {
    const node = nodeInput.value.trim();
    const amt = parseInt(amountInput.value);
    
    if (!node) {
        showStatus('Please enter a node ID', true);
        return;
    }
    
    if (isNaN(amt) || amt <= 0) {
        showStatus('Please enter a valid stake amount', true);
        return;
    }

    try {
        const response = await fetch('/stake', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({node_id: node, amount: amt})
        });
        
        if (!response.ok) throw new Error('Network response was not ok');
        
        const data = await response.json();
        showStatus(`✅ ${data.message}`);
        
        // Clear inputs after successful stake
        nodeInput.value = '';
        amountInput.value = '';
        
    } catch (error) {
        showStatus(`❌ Error: ${error.message}`, true);
        console.error('Staking error:', error);
    }
}

// Mine/propose block function
async function mine() {
    try {
        mineStatus.style.display = 'block';
        mineStatus.textContent = '⏳ Selecting validator and proposing block...';
        mineStatus.className = 'status';
        
        const response = await fetch('/mine');
        if (!response.ok) throw new Error('Network response was not ok');
        
        const data = await response.json();
        mineStatus.textContent = `✅ ${data.message}`;
        mineStatus.className = 'status success';
        
        // Refresh the chain display
        await getChain();
        
    } catch (error) {
        mineStatus.textContent = `❌ Error: ${error.message}`;
        mineStatus.className = 'status error';
        console.error('Mining error:', error);
    }
}

// Get blockchain data function
async function getChain() {
    try {
        chainDisplay.textContent = 'Loading blockchain...';
        
        const response = await fetch('/chain');
        if (!response.ok) throw new Error('Network response was not ok');
        
        const data = await response.json();
        chainDisplay.textContent = JSON.stringify(data.chain, null, 2);
        
    } catch (error) {
        chainDisplay.textContent = `Error loading chain: ${error.message}`;
        console.error('Chain fetch error:', error);
    }
}

// Clear blockchain function
async function clearChain() {
    if (!confirm("⚠️ WARNING: This will DELETE the entire blockchain!\n\nAre you absolutely sure?")) {
        return;
    }

    try {
        const response = await fetch('/clear', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        });
        
        if (!response.ok) throw new Error('Network response was not ok');
        
        const data = await response.json();
        showStatus(`🔄 ${data.message}`);
        
        // Refresh the chain display
        await getChain();
        
    } catch (error) {
        showStatus(`❌ Error clearing chain: ${error.message}`, true);
        console.error('Clear chain error:', error);
    }
}

// Initial chain load when page loads
document.addEventListener('DOMContentLoaded', getChain);