/**
 * Script to update all hardcoded old backend URLs to use API_BASE_URL
 * Run this once to update all files
 * 
 * Usage: node update-api-urls.js
 */

const fs = require('fs');
const path = require('path');

const OLD_URL = 'https://caps-em1t.onrender.com';
const NEW_URL_VAR = 'API_BASE_URL'; // Will use from apiConfig

// Files to update (relative to frontend/my-app/src)
const filesToUpdate = [
  'pages/RegisterPage.tsx',
  'pages/HomePage.tsx',
  'pages/ProfilePage.tsx',
  'pages/ResetPassword.tsx',
  'pages/ResidentDashboard.tsx',
  'pages/VisitorDashboard.tsx',
  'pages/VisitorStatus.tsx',
  'pages/Contact.tsx',
  'pages/Map.tsx',
  'pages/UserMapPage.tsx',
  'pages/BookingAmenities.tsx',
  'pages/HouseDetailPage.tsx',
  'pages/HouseSalePage.tsx',
  'pages/AdminUsersPage.tsx',
  'pages/Messenger.tsx',
  'pages/Visitors.tsx',
  'pages/visitorsTracking.tsx',
  'pages/ResidentsApproval.tsx',
  'pages/Pins.tsx',
];

const srcDir = path.join(__dirname, 'src');

function updateFile(filePath) {
  const fullPath = path.join(srcDir, filePath);
  
  if (!fs.existsSync(fullPath)) {
    console.log(`⚠️  File not found: ${filePath}`);
    return false;
  }

  let content = fs.readFileSync(fullPath, 'utf8');
  let updated = false;
  let count = 0;

  // Replace hardcoded URLs with API_BASE_URL
  const patterns = [
    {
      // Pattern: 'https://caps-em1t.onrender.com/api/...'
      regex: /'https:\/\/caps-em1t\.onrender\.com(\/api\/[^']+)'/g,
      replacement: (match, endpoint) => {
        updated = true;
        count++;
        return `\`\${API_BASE_URL}${endpoint}\``;
      }
    },
    {
      // Pattern: "https://caps-em1t.onrender.com/api/..."
      regex: /"https:\/\/caps-em1t\.onrender\.com(\/api\/[^"]+)"/g,
      replacement: (match, endpoint) => {
        updated = true;
        count++;
        return `\`\${API_BASE_URL}${endpoint}\``;
      }
    },
    {
      // Pattern: `https://caps-em1t.onrender.com${...}`
      regex: /`https:\/\/caps-em1t\.onrender\.com\$\{([^}]+)\}`/g,
      replacement: (match, varName) => {
        updated = true;
        count++;
        return `\`\${API_BASE_URL}\${${varName}}\``;
      }
    },
    {
      // Pattern: https://caps-em1t.onrender.com${...} (in template strings)
      regex: /https:\/\/caps-em1t\.onrender\.com\$\{([^}]+)\}/g,
      replacement: (match, varName) => {
        updated = true;
        count++;
        return `\${API_BASE_URL}\${${varName}}`;
      }
    }
  ];

  patterns.forEach(pattern => {
    content = content.replace(pattern.regex, pattern.replacement);
  });

  if (updated) {
    // Check if API_BASE_URL is imported, if not add it
    if (!content.includes("import { API_BASE_URL }") && !content.includes('from "../utils/apiConfig"')) {
      // Find the last import statement
      const importMatch = content.match(/(import .+ from ['"].+['"];?\n?)+/);
      if (importMatch) {
        const lastImport = importMatch[0].split('\n').filter(l => l.trim()).pop();
        const insertIndex = content.indexOf(lastImport) + lastImport.length;
        content = content.slice(0, insertIndex) + 
                  `\nimport { API_BASE_URL } from '../utils/apiConfig';` + 
                  content.slice(insertIndex);
      }
    }

    fs.writeFileSync(fullPath, content, 'utf8');
    console.log(`✅ Updated ${filePath} (${count} replacements)`);
    return true;
  } else {
    console.log(`⏭️  No changes needed: ${filePath}`);
    return false;
  }
}

console.log('🔄 Updating API URLs...\n');

let totalUpdated = 0;
filesToUpdate.forEach(file => {
  if (updateFile(file)) {
    totalUpdated++;
  }
});

console.log(`\n✅ Complete! Updated ${totalUpdated} files.`);
console.log('\n⚠️  Note: Please review the changes and test your application.');
console.log('Some files may need manual adjustment for edge cases.');

