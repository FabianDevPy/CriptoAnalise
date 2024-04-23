const tabs = document.querySelectorAll('.tab');
            const contents = document.querySelectorAll('.content');
            const themeToggle = document.getElementById('themeToggle');
            const darkLabel = document.getElementById('darkLabel');
            const lightLabel = document.getElementById('lightLabel');

            tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                tabs.forEach(t => {
                    if (t.classList.contains('inactive')) {
                        t.classList.remove('inactive');
                        t.classList.add('active');
                    }
                    if (tab !== t) {
                        t.classList.add('inactive');
                        t.classList.remove('active');
                    }
                    
                });
                
                const activeTab = tab.getAttribute('data-tab');
                contents.forEach(content => {
                if (content.id === activeTab) {
                    content.classList.remove('hidden');   
                } else {
                    content.classList.add('hidden');
                }
                });
            });
            });

            themeToggle.addEventListener('change', () => {
            document.body.classList.toggle('dark');
            if (document.body.classList.contains('dark')) {
                darkLabel.style.display = 'none';
                lightLabel.style.display = 'inline';
            } else {
                darkLabel.style.display = 'inline';
                lightLabel.style.display = 'none';
            }
            });

            // Check initial theme preference
            if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.body.classList.add('dark');
            darkLabel.style.display = 'none';
            } else {
            lightLabel.style.display = 'none';
            }

            
