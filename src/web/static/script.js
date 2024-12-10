// src/web/static/script.js
document.getElementById('matchingForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Collect form data
    const formData = {};
    
    // Basic information
    formData.Child_Nickname = document.getElementById('Child_Nickname').value;
    formData.Child_Age = parseInt(document.getElementById('Child_Age').value);
    formData.Child_Gender = document.getElementById('Child_Gender').value;
    formData.Child_Region = document.getElementById('Child_Region').value;
    
    // Interests - 興味のリストとカラム名の処理を修正
    const interests = [
        'Science',
        'Coding/Game Design',
        'Reading/Writing',
        'Engineering',
        'Art',
        'Music',
        'Math'
    ];
    
    console.log("\nDebug: Processing interests in form submission");
    interests.forEach(interest => {
        const columnName = `Interest_${interest.replace('/', '_')}`;
        const element = document.getElementById(columnName);
        const value = element ? (element.checked ? 'Selected' : 'Not selected') : null;
        formData[columnName] = value;
        console.log(`Interest: ${interest}`);
        console.log(`Column name: ${columnName}`);
        console.log(`Value: ${value}`);
        console.log(`Element found: ${!!element}`);
    });
    
    // Availability
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    const times = ['Morning', 'Afternoon', 'Evening'];
    days.forEach(day => {
        times.forEach(time => {
            const id = `Available_Time_${day}_${time}`;
            formData[id] = document.getElementById(id).checked ? 'Available' : 'Not available';
        });
    });
    
    // Preferences
    const preferences = ['Interaction_Outside_Class', 'Overlapping_Time', 'Similar_Age', 'Same_Gender'];
    preferences.forEach(pref => {
        formData[`Preference_${pref}`] = document.getElementById(`Preference_${pref}`).value;
    });
    
    try {
        // Send data to server
        const response = await fetch('/match', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const matches = await response.json();
        displayMatches(matches);
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while finding matches. Please try again.');
    }
});

function displayMatches(matches) {
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = '<h2>Matching Results</h2>';
    
    matches.forEach(match => {
        const matchCard = document.createElement('div');
        matchCard.className = 'match-card';
        
        const score = (match.similarity_score * 100).toFixed(1);
        
        matchCard.innerHTML = `
            <div class="match-score">Match Score: ${score}%</div>
            <div class="match-details">
                <p><strong>Nickname:</strong> ${match.student.Child_Nickname}</p>
                <p><strong>Age:</strong> ${match.student.Child_Age}</p>
                <p><strong>Gender:</strong> ${match.student.Child_Gender}</p>
                <p><strong>Region:</strong> ${match.student.Child_Region}</p>
                
                <div class="match-interests">
                    <strong>Shared Interests:</strong>
                    <div>
                        ${match.shared_interests.map(interest => 
                            `<span class="tag">${interest}</span>`
                        ).join('')}
                    </div>
                </div>
                
                <div class="match-availability">
                    <strong>Overlapping Availability:</strong>
                    <div>
                        ${match.overlapping_availability.map(time => 
                            `<span class="tag">${time}</span>`
                        ).join('')}
                    </div>
                </div>
            </div>
        `;
        
        resultsContainer.appendChild(matchCard);
    });
} 