mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"uday@pharma-ci.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
[theme]\n\
primaryColor = \"#667eea\"\n\
backgroundColor = \"#ffffff\"\n\
secondaryBackgroundColor = \"#f0f2f6\"\n\
textColor = \"#262730\"\n\
" > ~/.streamlit/config.toml
