// Search and Filter functionality for Business and Professional Directories

class DirectorySearch {
    constructor(containerSelector, resultsSelector, searchInputSelector, filterSelectors) {
        this.container = document.querySelector(containerSelector);
        this.resultsContainer = document.querySelector(resultsSelector);
        this.searchInput = document.querySelector(searchInputSelector);
        this.filters = {};
        
        // Initialize filter elements
        filterSelectors.forEach(selector => {
            const element = document.querySelector(selector);
            if (element) {
                const filterName = element.name;
                this.filters[filterName] = element;
            }
        });
        
        this.debounceTimer = null;
        this.init();
    }
    
    init() {
        if (!this.container) return;
        
        // Add event listeners
        if (this.searchInput) {
            this.searchInput.addEventListener('input', () => this.handleSearchInput());
        }
        
        Object.values(this.filters).forEach(filter => {
            filter.addEventListener('change', () => this.handleFilterChange());
        });
        
        // Store original results for filtering
        this.storeOriginalResults();
    }
    
    storeOriginalResults() {
        const items = this.resultsContainer.querySelectorAll('.business-card, .professional-card');
        this.originalResults = Array.from(items).map(item => ({
            element: item,
            text: item.textContent.toLowerCase(),
            category: item.dataset.category?.toLowerCase() || '',
            location: item.dataset.location?.toLowerCase() || '',
            skills: item.dataset.skills?.toLowerCase() || '',
            role: item.dataset.role?.toLowerCase() || ''
        }));
    }
    
    handleSearchInput() {
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => {
            this.filterResults();
        }, 300); // Debounce for 300ms
    }
    
    handleFilterChange() {
        this.filterResults();
    }
    
    filterResults() {
        const searchTerm = this.searchInput?.value.toLowerCase() || '';
        const filterValues = {};
        
        Object.entries(this.filters).forEach(([name, element]) => {
            filterValues[name] = element.value.toLowerCase();
        });
        
        let visibleCount = 0;
        
        this.originalResults.forEach(result => {
            let visible = true;
            
            // Search term filter
            if (searchTerm && !result.text.includes(searchTerm)) {
                visible = false;
            }
            
            // Category filter (for businesses)
            if (filterValues.category && filterValues.category !== '' && 
                result.category !== filterValues.category) {
                visible = false;
            }
            
            // Location filter (for businesses)
            if (filterValues.location && filterValues.location !== '' && 
                !result.location.includes(filterValues.location)) {
                visible = false;
            }
            
            // Skill filter (for professionals)
            if (filterValues.skill && filterValues.skill !== '' && 
                !result.skills.includes(filterValues.skill)) {
                visible = false;
            }
            
            // Show/hide element
            if (visible) {
                result.element.style.display = '';
                visibleCount++;
            } else {
                result.element.style.display = 'none';
            }
        });
        
        // Update results count
        this.updateResultsCount(visibleCount);
        
        // Show/hide no results message
        this.toggleNoResults(visibleCount === 0);
    }
    
    updateResultsCount(count) {
        const resultsInfo = document.querySelector('.results-info');
        if (resultsInfo) {
            const plural = count !== 1 ? 's' : '';
            const type = this.container.classList.contains('professionals-page') ? 
                'professional' : 'business';
            resultsInfo.querySelector('p').textContent = 
                `Found ${count} ${type}${count !== 1 ? 'es' : ''}`;
        }
    }
    
    toggleNoResults(show) {
        let noResults = this.resultsContainer.querySelector('.no-results-instant');
        
        if (show) {
            if (!noResults) {
                noResults = document.createElement('div');
                noResults.className = 'no-results no-results-instant';
                noResults.innerHTML = `
                    <h3>No results found</h3>
                    <p>Try adjusting your search criteria</p>
                `;
                this.resultsContainer.appendChild(noResults);
            }
            noResults.style.display = 'block';
        } else if (noResults) {
            noResults.style.display = 'none';
        }
    }
    
    clearFilters() {
        if (this.searchInput) {
            this.searchInput.value = '';
        }
        
        Object.values(this.filters).forEach(filter => {
            filter.value = '';
        });
        
        this.filterResults();
    }
}

// Auto-complete functionality for search inputs
class SearchAutocomplete {
    constructor(inputSelector, suggestionsData) {
        this.input = document.querySelector(inputSelector);
        this.suggestions = suggestionsData;
        this.suggestionsList = null;
        this.init();
    }
    
    init() {
        if (!this.input) return;
        
        // Create suggestions container
        this.suggestionsList = document.createElement('div');
        this.suggestionsList.className = 'search-suggestions';
        this.input.parentElement.appendChild(this.suggestionsList);
        
        // Add event listeners
        this.input.addEventListener('input', (e) => this.handleInput(e));
        this.input.addEventListener('blur', () => {
            setTimeout(() => this.hideSuggestions(), 200);
        });
        
        document.addEventListener('click', (e) => {
            if (!this.input.contains(e.target)) {
                this.hideSuggestions();
            }
        });
    }
    
    handleInput(e) {
        const value = e.target.value.toLowerCase();
        
        if (value.length < 2) {
            this.hideSuggestions();
            return;
        }
        
        const matches = this.suggestions.filter(item => 
            item.toLowerCase().includes(value)
        ).slice(0, 5);
        
        if (matches.length > 0) {
            this.showSuggestions(matches);
        } else {
            this.hideSuggestions();
        }
    }
    
    showSuggestions(matches) {
        this.suggestionsList.innerHTML = matches.map(match => 
            `<div class="suggestion-item">${this.highlightMatch(match, this.input.value)}</div>`
        ).join('');
        
        this.suggestionsList.style.display = 'block';
        
        // Add click handlers
        this.suggestionsList.querySelectorAll('.suggestion-item').forEach((item, index) => {
            item.addEventListener('click', () => {
                this.input.value = matches[index];
                this.hideSuggestions();
                this.input.dispatchEvent(new Event('input'));
            });
        });
    }
    
    highlightMatch(text, query) {
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<strong>$1</strong>');
    }
    
    hideSuggestions() {
        this.suggestionsList.style.display = 'none';
    }
}

// Export for use in pages
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { DirectorySearch, SearchAutocomplete };
}
