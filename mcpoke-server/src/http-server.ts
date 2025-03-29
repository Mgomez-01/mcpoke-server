/**
 * HTTP server for serving cached sprites
 */
import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { debugLog, debugError } from './utils/debug.js';
import { tools } from './server.js';

// Get the current directory when using ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Calculate base paths
const PROJECT_ROOT = path.resolve(__dirname, '../');
const ASSETS_DIR = path.join(PROJECT_ROOT, 'assets');
const SPRITES_DIR = path.join(ASSETS_DIR, 'sprites');
const ARTWORK_DIR = path.join(ASSETS_DIR, 'artwork');

// MIME types map
const MIME_TYPES: Record<string, string> = {
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.json': 'application/json',
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'text/javascript',
  '.txt': 'text/plain'
};

/**
 * Create and start an HTTP server for serving cached sprites
 * @param port The port to listen on
 * @returns The HTTP server instance
 */
export function startHttpServer(port: number = 8080): http.Server {
  const server = http.createServer((req, res) => {
    debugLog('HttpServer', `Received request: ${req.method} ${req.url}`);

    // Parse URL
    const url = new URL(req.url || '/', `http://${req.headers.host}`);
    const pathname = decodeURIComponent(url.pathname);

    // Handle MCP API requests
    if (pathname === '/api/mcp' && req.method === 'POST') {
      handleMCPRequest(req, res);
      return;
    }
    
    // Serve only files from specific directories
    let filePath = '';
    
    if (pathname.startsWith('/sprites/')) {
      filePath = path.join(SPRITES_DIR, pathname.substring('/sprites/'.length));
    } else if (pathname.startsWith('/artwork/')) {
      filePath = path.join(ARTWORK_DIR, pathname.substring('/artwork/'.length));
    } else {
      // Not Found - Only sprites and artwork are allowed
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('Not Found');
      return;
    }

    // Check if file exists
    fs.stat(filePath, (err, stats) => {
      if (err || !stats.isFile()) {
        debugError('HttpServer', err || new Error('Not a file'), `File not found: ${filePath}`);
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found');
        return;
      }

      // Determine content type based on extension
      const ext = path.extname(filePath).toLowerCase();
      const contentType = MIME_TYPES[ext] || 'application/octet-stream';

      // Add cache headers - 1 day for sprites
      const cacheControl = 'public, max-age=86400';

      // Read and serve file
      fs.readFile(filePath, (err, data) => {
        if (err) {
          debugError('HttpServer', err, `Error reading file: ${filePath}`);
          res.writeHead(500, { 'Content-Type': 'text/plain' });
          res.end('Internal Server Error');
          return;
        }

        // Success! Serve the file
        res.writeHead(200, {
          'Content-Type': contentType,
          'Content-Length': stats.size,
          'Cache-Control': cacheControl
        });
        res.end(data);
        debugLog('HttpServer', `Served file: ${filePath} (${stats.size} bytes)`);
      });
    });
  });

  // Start listening
  server.listen(port, () => {
    console.error(`HTTP server for sprites listening on port ${port}`);
    debugLog('HttpServer', `Started on port ${port}`);
  });

  return server;
}

/**
 * Handle MCP API requests
 * @param req The HTTP request
 * @param res The HTTP response
 */
function handleMCPRequest(req: http.IncomingMessage, res: http.ServerResponse) {
  debugLog('HttpServer', 'Handling MCP API request');
  
  // Collect request body
  let body = '';
  req.on('data', (chunk) => {
    body += chunk.toString();
  });
  
  req.on('end', async () => {
    try {
      // Parse the request
      const request = JSON.parse(body);
      debugLog('HttpServer', `MCP request: ${JSON.stringify(request)}`);
      
      // Check if this is a valid MCP request
      if (!request.jsonrpc || request.jsonrpc !== '2.0' || !request.method) {
        throw new Error('Invalid MCP request format');
      }
      
      let result;
      
      // Handle different MCP request types
      if (request.method === 'ping') {
        // Simple ping response
        result = { status: 'ok', message: 'MCPoke server is running' };
      } else if (request.method === 'tools/list') {
        // List available tools
        const toolsList = Object.entries(tools).map(([name, _]) => ({
          name,
          description: getToolDescription(name)
        }));
        
        result = { tools: toolsList };
      } else if (request.method === 'call_tool') {
        // Call a specific tool
        const { name, arguments: args } = request.params;
        
        if (!name || !tools[name]) {
          throw new Error(`Unknown tool: ${name}`);
        }
        
        // Execute the tool
        const toolResult = await tools[name](args || {});
        result = toolResult;
      } else {
        throw new Error(`Unknown method: ${request.method}`);
      }
      
      // Send the response
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        jsonrpc: '2.0',
        id: request.id,
        result: result
      }));
      
    } catch (error: any) {
      debugError('HttpServer', error, 'Error handling MCP request');
      
      // Send error response
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        jsonrpc: '2.0',
        id: (body && JSON.parse(body).id) || null,
        error: {
          code: -32000,
          message: error.message || 'Unknown error'
        }
      }));
    }
  });
  
  req.on('error', (error) => {
    debugError('HttpServer', error, 'Error reading request body');
    
    // Send error response
    res.writeHead(500, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      jsonrpc: '2.0',
      id: null,
      error: {
        code: -32000,
        message: 'Error reading request body'
      }
    }));
  });
}

/**
 * Get the description for a tool
 * @param name The tool name
 * @returns The tool description
 */
function getToolDescription(name: string): string {
  const descriptions: Record<string, string> = {
    'get_pokemon': 'Get detailed information about a Pokémon by name or ID',
    'search_pokemon': 'Search for Pokémon by partial name match',
    'compare_pokemon': 'Compare multiple Pokémon side by side',
    'get_ability': 'Get information about a Pokémon ability by name or ID',
    'get_type': 'Get information about a Pokémon type by name or ID',
    'get_type_effectiveness': 'Calculate type effectiveness between attacking and defending types',
    'get_move': 'Get information about a Pokémon move by name or ID',
    'download_sprites': 'Download and cache all sprites for a Pokémon',
    'check_sprite_cache': 'Check if sprites for a Pokémon are cached locally',
    'bulk_download_sprites': 'Download sprites for a range of Pokémon IDs',
    'get_sprite_cache_stats': 'Get statistics about cached sprites',
    'clear_sprite_cache': 'Clear the sprite cache'
  };
  
  return descriptions[name] || 'No description available';
}
