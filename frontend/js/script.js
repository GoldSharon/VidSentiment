const API_URL = 'http://127.0.0.1:8000';
        let sentimentChart;
        async function analyzeComments() {
            const videoLink = document.getElementById("videoLink").value;
            const resultsDiv = document.getElementById("results");
            const loadingDiv = document.getElementById("loading");
            const resultsSection = document.getElementById("resultsSection");

            if (!videoLink) {
                alert("Please enter a YouTube video link.");
                return;
            }

            resultsDiv.innerHTML = "";
            loadingDiv.style.display = "block";
            resultsSection.style.display = "block"; // Show results section

            try {
                const response = await fetch(`${API_URL}/analyze_comments/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ link: videoLink })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                loadingDiv.style.display = "none";

                if (data.error) {
                    resultsDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
                } else {
                    const sentimentHTML = Object.entries(data.sentiment_counts)
                        .map(([sentiment, count]) => `<li><strong>${sentiment}:</strong> ${count}</li>`)
                        .join('');

                    const commentsHTML = data.top_comments
                        .map(comment => `
                            <div class="comment-card">
                                <div class="comment-author">${comment.Author}</div>
                                <div class="comment-text">${comment.Comment}</div>
                                <div class="comment-likes">${comment.Likes} likes</div>
                            </div>
                        `)
                        .join('');

                    // Render Horizontal Bar Chart
                    const ctx = document.createElement('canvas');
                    ctx.id = 'sentimentChart';
                    resultsDiv.innerHTML = `
                        <h3>Results</h3>
                        <p><strong>Title:</strong> ${data.title}</p>
                        <p><strong>Publish Date:</strong> ${data.publish_date}</p>
                        <p><strong>Views:</strong> ${data.views}</p>
                        <p><strong>Total Comments:</strong> ${data.total_comments}</p>
                        <h4>Sentiment Analysis:</h4>
                        <div class="chart-container">
                            <canvas id="sentimentChart"></canvas>
                        </div>
                        <h4>Top Comments:</h4>
                        <div>${commentsHTML}</div>
                    `;

                    renderSentimentChart(data.sentiment_counts);

                    // Initialize Chart.js for Horizontal Bar Chart
                    
                }
            } catch (error) {
                loadingDiv.style.display = "none";
                resultsDiv.innerHTML = `<p class="error">Failed to fetch data. Please try again. Error: ${error.message}</p>`;
            }

        }
        function renderSentimentChart(sentimentData) {
            const ctx = document.getElementById("sentimentChart").getContext("2d");

            if (sentimentChart) {
                sentimentChart.destroy();
            }

            sentimentChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: Object.keys(sentimentData),
                    datasets: [{
                        label: 'Sentiment Count',
                        data: Object.values(sentimentData),
                        backgroundColor: ['#ff758c', '#ff9a9e', '#fad0c4'],
                        borderColor: ['#ff416c', '#ff6b6b', '#f8a5c2'],
                        borderWidth: 1,
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Count',
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Sentiment',
                            }
                        }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            });
        }
        