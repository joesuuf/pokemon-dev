import { VercelRequest, VercelResponse } from '@vercel/node'

/**
 * Serverless function to proxy Pokemon TCG API requests
 * This solves the CORS issue by acting as a backend proxy
 *
 * Route: /api/cards
 * Methods: GET
 * Query params: q (search query), pageSize (results per page)
 */

export default async function handler(
  request: VercelRequest,
  response: VercelResponse
): Promise<void> {
  // Only allow GET requests
  if (request.method !== 'GET') {
    return response.status(405).json({ error: 'Method not allowed' })
  }

  try {
    // Get query parameters from the request
    const { q, pageSize = '20' } = request.query

    // Validate required parameters
    if (!q || typeof q !== 'string') {
      return response.status(400).json({
        error: 'Missing required parameter: q (search query)',
      })
    }

    // Get API key from environment variable
    const apiKey = process.env.POKEMON_TCG_API_KEY
    if (!apiKey) {
      console.error('POKEMON_TCG_API_KEY not set in environment')
      return response.status(500).json({
        error: 'Server configuration error - API key not found',
      })
    }

    // Build the URL for the Pokemon TCG API
    const apiUrl = new URL('https://api.pokemontcg.io/v2/cards')
    apiUrl.searchParams.append('q', q)
    apiUrl.searchParams.append('pageSize', String(pageSize))

    console.log(`[Pokemon TCG Proxy] Fetching: ${apiUrl.toString()}`)

    // Make the request to Pokemon TCG API
    const apiResponse = await fetch(apiUrl.toString(), {
      method: 'GET',
      headers: {
        'X-Api-Key': apiKey,
        'Content-Type': 'application/json',
        'User-Agent': 'Pokemon-TCG-Search/1.0 (Vercel Serverless)',
      },
    })

    // Check if the API response is successful
    if (!apiResponse.ok) {
      console.error(
        `[Pokemon TCG Proxy] API error: ${apiResponse.status} ${apiResponse.statusText}`
      )

      // Return appropriate error response
      let errorData
      try {
        errorData = await apiResponse.json()
      } catch {
        errorData = { error: `API returned ${apiResponse.status}` }
      }

      return response.status(apiResponse.status).json({
        error: 'Failed to fetch from Pokemon TCG API',
        details: errorData,
      })
    }

    // Parse the JSON response
    const data = await apiResponse.json()

    // Set CORS headers to allow frontend requests
    response.setHeader('Access-Control-Allow-Origin', '*')
    response.setHeader(
      'Access-Control-Allow-Methods',
      'GET, OPTIONS, HEAD'
    )
    response.setHeader(
      'Access-Control-Allow-Headers',
      'Content-Type'
    )

    // Set cache headers for performance
    response.setHeader('Cache-Control', 'public, max-age=300, s-maxage=300')

    // Return the proxied response
    console.log(
      `[Pokemon TCG Proxy] Success: Returning ${data.data?.length || 0} cards`
    )
    return response.status(200).json(data)
  } catch (error) {
    const errorMessage =
      error instanceof Error ? error.message : 'Unknown error'
    console.error(`[Pokemon TCG Proxy] Error: ${errorMessage}`)

    return response.status(500).json({
      error: 'Internal server error',
      message:
        process.env.NODE_ENV === 'development'
          ? errorMessage
          : 'An error occurred while fetching card data',
    })
  }
}
