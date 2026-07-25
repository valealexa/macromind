st.markdown("""
    <script>
        // Cambia il titolo dinamicamente nell'intestazione di iOS
        window.top.document.title = "MacroMind";
        
        // Inietta l'icona fitness direttamente nel document root dell'iframe principale
        var link = window.top.document.querySelector("link[rel*='icon']") || window.top.document.createElement('link');
        link.type = 'image/x-icon';
        link.rel = 'shortcut icon';
        link.href = 'https://img.icons8.com/emoji/192/dumbbell-emoji.png';
        window.top.document.getElementsByTagName('head')[0].appendChild(link);

        var appleLink = window.top.document.createElement('link');
        appleLink.rel = 'apple-touch-icon';
        appleLink.href = 'https://img.icons8.com/emoji/192/dumbbell-emoji.png';
        window.top.document.getElementsByTagName('head')[0].appendChild(appleLink);
    </script>
""", unsafe_allow_html=True)
