const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

// Directory containing placeholder .md files
const placeholdersDir = path.join(__dirname, 'docs', 'images', 'diagrams');
// Output directory for PNG images (same as placeholders)
const outputDir = path.join(__dirname, 'docs', 'images', 'diagrams');

// Create output directory if it doesn't exist
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// Function to extract Mermaid code from markdown file
function extractMermaidCode(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const mermaidMatch = content.match(/```mermaid\n([\s\S]*?)```/);
  
  if (mermaidMatch && mermaidMatch[1]) {
    return mermaidMatch[1].trim();
  }
  
  console.error(`No Mermaid code found in ${filePath}`);
  return null;
}

// Function to generate a PNG from Mermaid code using the CLI
async function generatePNG(mermaidCode, outputPath) {
  // Create a temporary file for the Mermaid code
  const tempFile = path.join(__dirname, 'temp-diagram.mmd');
  fs.writeFileSync(tempFile, mermaidCode);
  
  try {
    // Run the Mermaid CLI command
    console.log(`Generating: ${outputPath}`);
    await execPromise(`npx @mermaid-js/mermaid-cli -i "${tempFile}" -o "${outputPath}"`);
    console.log(`Successfully generated: ${outputPath}`);
    return true;
  } catch (error) {
    console.error(`Error generating diagram: ${error.message}`);
    return false;
  } finally {
    // Clean up the temporary file
    if (fs.existsSync(tempFile)) {
      fs.unlinkSync(tempFile);
    }
  }
}

// Process all placeholder files
async function processAllDiagrams() {
  try {
    const files = fs.readdirSync(placeholdersDir);
    
    // Filter to only get the .png.md placeholder files
    const placeholderFiles = files.filter(file => file.endsWith('.png.md'));
    console.log(`Found ${placeholderFiles.length} placeholder files to process.`);
    
    // Process each file
    for (const file of placeholderFiles) {
      const filePath = path.join(placeholdersDir, file);
      const mermaidCode = extractMermaidCode(filePath);
      
      if (mermaidCode) {
        // Output PNG path is the same as the placeholder but without the .md extension
        const outputPath = path.join(outputDir, file.replace('.md', ''));
        await generatePNG(mermaidCode, outputPath);
      }
    }
    
    console.log('All diagrams processed!');
  } catch (error) {
    console.error(`Error processing diagrams: ${error.message}`);
  }
}

// Run the processing function
processAllDiagrams();
