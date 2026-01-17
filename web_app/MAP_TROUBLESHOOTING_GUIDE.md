# Map Display Troubleshooting Guide

## Issue: Mines Data Not Showing on Map

This guide helps diagnose and fix issues where mine locations aren't appearing on the interactive map in the dashboard.

---

## Quick Diagnosis

### 1. Backend Test (✓ VERIFIED WORKING)
Run the diagnostic script to verify backend is working:
```bash
python test_map_data.py
```

**Expected Output:**
- ✓ 18 mines loaded
- ✓ All predictions working
- ✓ All coordinates valid
- Risk distribution: 5 HIGH, 4 MEDIUM, 9 LOW

### 2. API Connection Test
Visit the API test page: `http://localhost:5000/api_test`

Click "Run Test" on each section to verify:
- ✓ `/api/predictions` returns 18 mines
- ✓ Coordinates are in correct format: `[latitude, longitude]`
- ✓ No CORS errors
- ✓ Response time < 1000ms

### 3. Browser Console Check
1. Open dashboard in browser
2. Press F12 to open Developer Tools
3. Go to "Console" tab
4. Refresh page
5. Look for JavaScript errors (red text)

---

## Common Issues & Solutions

### Issue 1: No Markers Appearing (Map Loads but Empty)

**Symptoms:**
- Map displays correctly
- No colored markers visible
- Statistics show "0" for all risk levels

**Possible Causes & Solutions:**

#### A. JavaScript Error During Marker Creation
1. Open browser console (F12)
2. Look for errors like:
   - `Uncaught TypeError: Cannot read property 'coordinates'`
   - `L is not defined` (Leaflet not loaded)
   
**Solution:**
- Check if Leaflet library is loaded:
  ```javascript
  // In browser console
  console.log(typeof L);  // Should be "object"
  ```
- If `undefined`, check internet connection (CDN blocked)
- Add console.log in `updateMineMarkers()`:
  ```javascript
  function updateMineMarkers(predictions) {
      console.log('Updating markers, predictions:', predictions);
      console.log('Number of predictions:', predictions.length);
      // ... rest of function
  }
  ```

#### B. Map Not Initialized Before Markers Added
**Solution:** Add initialization check in dashboard.html:
```javascript
function loadMines() {
    // Wait for map to be ready
    if (!map) {
        console.error('Map not initialized!');
        setTimeout(loadMines, 1000);
        return;
    }
    
    fetch('/api/predictions')
        .then(response => response.json())
        .then(data => {
            console.log('Loaded predictions:', data.length);
            updateMineMarkers(data);
            updateStatistics(data);
        })
        .catch(error => {
            console.error('Error loading mines:', error);
            showNotification('Failed to load mine data', 'danger');
        });
}
```

#### C. API Returns Empty Array
Run this in browser console:
```javascript
fetch('/api/predictions')
    .then(r => r.json())
    .then(data => console.log('API Response:', data));
```

**If empty:**
1. Check Flask app is running: `ps aux | grep python` (Linux/Mac) or `Get-Process python` (Windows)
2. Check for server errors in Flask console
3. Restart Flask app

---

### Issue 2: Some Markers Missing (Partial Display)

**Symptoms:**
- Some mines appear, others don't
- Statistics show correct total but fewer markers

**Possible Causes & Solutions:**

#### A. Invalid Coordinates for Some Mines
Run coordinate validation:
```javascript
fetch('/api/predictions')
    .then(r => r.json())
    .then(predictions => {
        predictions.forEach(p => {
            const [lat, lon] = p.coordinates;
            if (lat < -90 || lat > 90 || lon < -180 || lon > 180) {
                console.error('Invalid coordinates:', p.mine_name, p.coordinates);
            }
        });
    });
```

**Solution:** Fix coordinates in `data_service.py` if any are invalid.

#### B. Markers Outside Map View
Some mines might be outside the initial map view.

**Solution:** Add auto-fit bounds in dashboard.html:
```javascript
function updateMineMarkers(predictions) {
    // ... existing marker creation code ...
    
    // Auto-fit map to show all markers
    if (Object.keys(mineMarkers).length > 0) {
        const markerBounds = L.featureGroup(Object.values(mineMarkers));
        map.fitBounds(markerBounds.getBounds(), { padding: [50, 50] });
    }
}
```

#### C. Async Loading Race Condition
**Solution:** Add loading state and error handling:
```javascript
let isLoadingMines = false;

function loadMines() {
    if (isLoadingMines) {
        console.log('Already loading mines...');
        return;
    }
    
    isLoadingMines = true;
    
    fetch('/api/predictions')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log(`Successfully loaded ${data.length} mines`);
            updateMineMarkers(data);
            updateStatistics(data);
        })
        .catch(error => {
            console.error('Error loading mines:', error);
            showNotification('Failed to load mine data: ' + error.message, 'danger');
        })
        .finally(() => {
            isLoadingMines = false;
        });
}
```

---

### Issue 3: Map Not Loading At All

**Symptoms:**
- Blank space where map should be
- "Loading..." message persists

**Possible Causes & Solutions:**

#### A. Leaflet CDN Blocked
**Check:** Open browser console, look for:
```
Failed to load resource: net::ERR_BLOCKED_BY_CLIENT
```

**Solution:** 
1. Disable ad blockers temporarily
2. Or download Leaflet locally:
   ```bash
   mkdir -p static/css static/js
   wget https://unpkg.com/leaflet@1.7.1/dist/leaflet.css -O static/css/leaflet.css
   wget https://unpkg.com/leaflet@1.7.1/dist/leaflet.js -O static/js/leaflet.js
   ```
3. Update dashboard.html:
   ```html
   <link href="{{ url_for('static', filename='css/leaflet.css') }}" rel="stylesheet">
   <script src="{{ url_for('static', filename='js/leaflet.js') }}"></script>
   ```

#### B. Map Container Height Issue
**Check:** Map container has zero height

**Solution:** Add explicit height in dashboard.html:
```css
#map {
    height: 500px !important;
    min-height: 500px;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}
```

#### C. Leaflet Initialization Error
**Solution:** Add error handling:
```javascript
function initializeMap() {
    try {
        if (typeof L === 'undefined') {
            console.error('Leaflet library not loaded!');
            document.getElementById('map').innerHTML = 
                '<div style="padding: 50px; text-align: center; color: red;">' +
                'Error: Map library failed to load. Please check your internet connection.</div>';
            return;
        }
        
        map = L.map('map').setView([20.5937, 78.9629], 5);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(map);
        
        console.log('Map initialized successfully');
    } catch (error) {
        console.error('Map initialization failed:', error);
        alert('Failed to initialize map: ' + error.message);
    }
}
```

---

### Issue 4: Markers Appear but Map is Blank/Gray

**Symptoms:**
- Mine markers visible
- Background tiles not loading (gray squares with grid)

**Solution:**

#### A. Tile Server Issue
Try alternative tile server in dashboard.html:
```javascript
// Replace OpenStreetMap with alternative
L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenTopoMap contributors'
}).addTo(map);

// Or use CartoDB
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
    attribution: '© CartoDB'
}).addTo(map);
```

#### B. Firewall/Proxy Blocking Tiles
**Check:** Network tab in Dev Tools for failed tile requests

**Solution:** Configure proxy or use local tile server

---

## Enhanced Debugging Tools

### 1. Add Debug Panel to Dashboard

Add this to dashboard.html after the map container:
```html
<div id="debug-panel" style="position: fixed; bottom: 10px; right: 10px; background: rgba(0,0,0,0.8); color: lime; padding: 10px; border-radius: 5px; font-family: monospace; font-size: 12px; z-index: 9999; max-width: 300px;">
    <div id="debug-content">Debug Info Loading...</div>
</div>

<script>
function updateDebugPanel() {
    const markers = Object.keys(mineMarkers).length;
    const mapReady = typeof map !== 'undefined' && map !== null;
    const leafletLoaded = typeof L !== 'undefined';
    
    document.getElementById('debug-content').innerHTML = `
        <strong>Debug Info:</strong><br>
        Leaflet Loaded: ${leafletLoaded ? '✓' : '✗'}<br>
        Map Initialized: ${mapReady ? '✓' : '✗'}<br>
        Markers on Map: ${markers}<br>
        Last Update: ${new Date().toLocaleTimeString()}
    `;
}

// Update debug panel every 2 seconds
setInterval(updateDebugPanel, 2000);
</script>
```

### 2. Verbose Logging

Replace the `loadMines()` function with this verbose version:
```javascript
function loadMines() {
    console.log('[loadMines] Starting mine data fetch...');
    console.log('[loadMines] Map object:', map);
    console.log('[loadMines] Current marker count:', Object.keys(mineMarkers).length);
    
    fetch('/api/predictions')
        .then(response => {
            console.log('[loadMines] Received response:', response.status, response.statusText);
            return response.json();
        })
        .then(data => {
            console.log('[loadMines] Parsed JSON data:', data);
            console.log('[loadMines] Mine count:', data.length);
            console.log('[loadMines] Sample mine data:', data[0]);
            
            updateMineMarkers(data);
            updateStatistics(data);
            
            console.log('[loadMines] Successfully processed all mines');
        })
        .catch(error => {
            console.error('[loadMines] ERROR:', error);
            console.error('[loadMines] Error stack:', error.stack);
            showNotification('Failed to load mine data', 'danger');
        });
}
```

---

## Step-by-Step Diagnostic Procedure

1. **Run Backend Test**
   ```bash
   python test_map_data.py
   ```
   ✓ Should show 18 mines with valid coordinates

2. **Access API Test Page**
   - Go to: `http://localhost:5000/api_test` (or `localhost:5050/api_test` for auth version)
   - Run all 5 tests
   - All should show green ✓ success

3. **Check Browser Console**
   - Open dashboard
   - Press F12
   - Go to Console tab
   - Look for red error messages

4. **Check Network Tab**
   - F12 → Network tab
   - Refresh page
   - Filter by "XHR" or "Fetch"
   - Click on `/api/predictions`
   - Check Response tab - should see JSON with 18 mines

5. **Verify Leaflet**
   - In Console tab, type: `console.log(L.version)`
   - Should print Leaflet version (e.g., "1.7.1")

6. **Manual Map Test**
   - In Console, type:
     ```javascript
     L.marker([20, 78]).addTo(map).bindPopup("Test").openPopup();
     ```
   - A marker should appear in central India with "Test" popup

---

## Quick Fixes

### Fix 1: Force Refresh Map Data
Add a "Force Refresh" button:
```javascript
function forceRefresh() {
    console.log('Force refreshing map data...');
    
    // Clear all markers
    Object.values(mineMarkers).forEach(marker => map.removeLayer(marker));
    mineMarkers = {};
    
    // Reload data
    loadMines();
    loadAlerts();
    
    showNotification('Map data refreshed', 'success');
}
```

### Fix 2: Add Retry Logic
```javascript
function loadMinesWithRetry(maxRetries = 3, retryDelay = 2000) {
    let attempts = 0;
    
    function attempt() {
        fetch('/api/predictions')
            .then(response => response.json())
            .then(data => {
                if (data.length === 0 && attempts < maxRetries) {
                    console.log(`Retry ${attempts + 1}/${maxRetries} - empty response`);
                    attempts++;
                    setTimeout(attempt, retryDelay);
                } else {
                    updateMineMarkers(data);
                    updateStatistics(data);
                }
            })
            .catch(error => {
                if (attempts < maxRetries) {
                    console.log(`Retry ${attempts + 1}/${maxRetries} - error:`, error);
                    attempts++;
                    setTimeout(attempt, retryDelay);
                } else {
                    console.error('All retries failed:', error);
                    showNotification('Failed to load mine data after ' + maxRetries + ' attempts', 'danger');
                }
            });
    }
    
    attempt();
}
```

### Fix 3: Fallback to Basic Markers
If Leaflet divIcons aren't working:
```javascript
function updateMineMarkers(predictions) {
    Object.values(mineMarkers).forEach(marker => map.removeLayer(marker));
    mineMarkers = {};
    
    predictions.forEach(prediction => {
        // Use basic circle markers instead of divIcons
        const marker = L.circleMarker([prediction.coordinates[0], prediction.coordinates[1]], {
            radius: 8,
            fillColor: getRiskColor(prediction.risk_level),
            color: '#fff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        })
        .bindPopup(createMinePopup(prediction))
        .addTo(map);
        
        mineMarkers[prediction.mine_id] = marker;
    });
    
    console.log(`Created ${Object.keys(mineMarkers).length} markers`);
}
```

---

## Still Having Issues?

If none of the above solutions work:

1. **Collect Debug Information:**
   ```bash
   # Save backend test output
   python test_map_data.py > debug_backend.txt
   
   # Save browser console output (copy from F12 console)
   # Save network requests (F12 → Network → Right-click → Save all as HAR)
   ```

2. **Check Alternative Dashboard:**
   - The authenticated version might work better: `http://localhost:5050/login`
   - Credentials: admin/admin123

3. **Create Minimal Test:**
   Create `test_simple_map.html` in templates:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"/>
       <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
       <style>#map { height: 500px; }</style>
   </head>
   <body>
       <div id="map"></div>
       <script>
           const map = L.map('map').setView([20, 78], 5);
           L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
           
           fetch('/api/predictions')
               .then(r => r.json())
               .then(data => {
                   console.log('Data:', data);
                   data.forEach(m => {
                       L.circleMarker(m.coordinates, {
                           radius: 10,
                           fillColor: m.risk_level === 'HIGH' ? 'red' : 'green'
                       }).addTo(map).bindPopup(m.mine_name);
                   });
               });
       </script>
   </body>
   </html>
   ```

---

## Contact & Support

If you've tried all solutions and still have issues, provide:
1. Output of `python test_map_data.py`
2. Browser console errors (screenshot or text)
3. Network tab showing `/api/predictions` response
4. Python/Flask version: `python --version`
5. Operating system and browser version

The issue is most likely one of:
- JavaScript error preventing marker creation
- Map not fully initialized before markers added
- API returning empty data (backend issue)
- Leaflet library not loading (CDN/firewall)
- Coordinate format mismatch

Use the debugging tools provided to identify which category your issue falls into.
