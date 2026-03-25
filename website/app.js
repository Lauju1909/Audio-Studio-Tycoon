// Audio Studio Tycoon - Mod Portal App
const MOCK_MODS = [
    {
        id: "cyberpunk_01",
        name: "Cyberpunk Theme Pack",
        author: "ModderX",
        downloads: "1.2k",
        rating: 4.8,
        color: "linear-gradient(135deg, #6e45e2, #88d3ce)"
    },
    {
        id: "retro_80s",
        name: "1980s Retro Sounds",
        author: "SynthWaveFan",
        downloads: "850",
        rating: 4.9,
        color: "linear-gradient(135deg, #ff00cc, #3333ff)"
    },
    {
        id: "medieval_ui",
        name: "Mittelalter Interface",
        author: "KnightCoder",
        downloads: "300",
        rating: 4.5,
        color: "linear-gradient(135deg, #fceabb, #f8b500)"
    }
];

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('modContainer');
    
    // Mods rendern
    MOCK_MODS.forEach(mod => {
        const card = document.createElement('div');
        card.className = 'mod-card glass';
        card.innerHTML = `
            <div class="mod-preview" style="background: ${mod.color};"></div>
            <div class="mod-info">
                <h3>${mod.name}</h3>
                <p>Von: ${mod.author}</p>
                <div class="stats">
                    <span>⬇️ ${mod.downloads}</span>
                    <span>⭐ ${mod.rating}</span>
                </div>
                <button class="btn-install" onclick="downloadMod('${mod.id}')">Download</button>
            </div>
        `;
        container.appendChild(card);
    });
});

function downloadMod(id) {
    alert("Download gestartet: " + id + ". In der finalen Version wird dies direkt mit dem Spiel synchronisiert!");
}
