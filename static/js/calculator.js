/**
 * This JavaScript file is responsible for dynamically updating the nutrition calculator on the Nutrition Hub page.
 * It retrieves the user's consumed calories and macronutrients from a JSON script tag, then updates the text
 * elements and visual bars to reflect the user's progress towards their daily goals.
 */

document.addEventListener('DOMContentLoaded', function() {
    const dataElement = document.getElementById('nutrition-data');

    if (dataElement) {
        try {
            const data = JSON.parse(dataElement.textContent);
            const consumed = data.consumed;
            const goals = data.goals;

            // --- 1. Update Text Elements ---
            document.getElementById('cal-consumed').innerText = consumed.calories;
            document.getElementById('cal-goal').innerText = goals.calories;

            const remaining = Math.max(0, goals.calories - consumed.calories);
            document.getElementById('cal-remaining').innerText = remaining;

            document.getElementById('prot-text').innerText = `${consumed.protein} / ${goals.protein} g`;
            document.getElementById('carb-text').innerText = `${consumed.carbs} / ${goals.carbs} g`;
            document.getElementById('fat-text').innerText = `${consumed.fats} / ${goals.fats} g`;

            // --- 2. Animate Macro Bars ---
            const protPct = Math.min(100, (consumed.protein / goals.protein) * 100);
            const carbPct = Math.min(100, (consumed.carbs / goals.carbs) * 100);
            const fatPct = Math.min(100, (consumed.fats / goals.fats) * 100);

            // Add  delay effect on load
            setTimeout(() => {
                document.getElementById('prot-bar').style.width = `${protPct}%`;
                document.getElementById('carb-bar').style.width = `${carbPct}%`;
                document.getElementById('fat-bar').style.width = `${fatPct}%`;
            }, 100);

            // --- 3. Calorie Ring ---
            const calPct = Math.min(100, (consumed.calories / goals.calories) * 100);
            const ring = document.getElementById('calorie-ring');

            // Get colors
            const style = getComputedStyle(document.body);
            const primaryColor = style.getPropertyValue('--primary-100').trim() || '#eb9c64';
            const bgMuted = style.getPropertyValue('--bg-300').trim() || '#c2baa6';

            // If over goal, make it red. Otherwise, use primary color.
            const ringColor = calPct >= 100 ? 'var(--primary-200)' : primaryColor;

            ring.style.background = `conic-gradient(${ringColor} ${calPct}%, ${bgMuted} 0)`;

        } catch (error) {
            console.error("Error parsing nutrition data:", error);
        }
    }
});