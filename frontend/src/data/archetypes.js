/**
 * MTG Archetypes by Format
 * Based on MTGGoldfish metagame data
 * Updated: December 2024
 */

export const ARCHETYPES_BY_FORMAT = {
  Standard: [
    'Azorius Control',
    'Domain Ramp',
    'Esper Midrange',
    'Golgari Midrange',
    'Mono Red Aggro',
    'Orzhov Midrange',
    'Rakdos Midrange',
    'Temur Rhinos',
    'Izzet Phoenix'
  ],

  Modern: [
    'Amulet Titan',
    'Burn',
    'Crashing Footfalls',
    'Death\'s Shadow',
    'Four-Color Control',
    'Hardened Scales',
    'Hammer Time',
    'Izzet Murktide',
    'Living End',
    'Mono Green Tron',
    'Rakdos Midrange',
    'Rhinos',
    'Scam (Grief)',
    'Temur Rhinos',
    'Yawgmoth'
  ],

  Pioneer: [
    'Abzan Greasefang',
    'Azorius Control',
    'Boros Convoke',
    'Izzet Phoenix',
    'Lotus Field Combo',
    'Mono Green Devotion',
    'Rakdos Midrange',
    'Rakdos Sacrifice',
    'Spirits',
    'Temur Rhinos',
    'Waste Not'
  ],

  Legacy: [
    'ANT (Storm)',
    'Death and Taxes',
    'Delver',
    'Elves',
    'Grixis Control',
    '8-Cast',
    'Lands',
    'Moon Stompy',
    'Painter',
    'Reanimator',
    'Sneak and Show',
    'TES (Storm)',
    'Turbo Depths'
  ],

  Vintage: [
    'Bazaar Hogaak',
    'Breach',
    'Doomsday',
    'Esper Control',
    'Jeskai',
    'Oath',
    'Paradoxical Outcome',
    'Shops',
    'Tinker',
    'White Eldrazi'
  ],

  Commander: [
    'Aggro',
    'Aristocrats',
    'Combo',
    'Control',
    'Group Hug',
    'Lands',
    'Midrange',
    'Reanimator',
    'Spellslinger',
    'Stax',
    'Stompy',
    'Tokens',
    'Tribal',
    'Voltron'
  ],

  Pauper: [
    'Affinity',
    'Azorius Familiars',
    'Boros Synthesizer',
    'Burn',
    'Caw-Gate',
    'Dimir Terror',
    'Elves',
    'Faeries',
    'Golgari Gardens',
    'Jeskai Ephemerate',
    'Kuldotha Red',
    'Mono Blue Terror',
    'Walls Combo'
  ]
}

// Common generic archetypes that work across formats
export const GENERIC_ARCHETYPES = [
  'Aggro',
  'Control',
  'Combo',
  'Midrange',
  'Ramp',
  'Tempo'
]

/**
 * Get archetypes for a specific format
 * @param {string} format - MTG format (Standard, Modern, etc.)
 * @returns {Array<string>} List of archetypes
 */
export function getArchetypesForFormat(format) {
  return ARCHETYPES_BY_FORMAT[format] || GENERIC_ARCHETYPES
}

/**
 * Get all unique archetypes across all formats
 * @returns {Array<string>} Sorted list of all archetypes
 */
export function getAllArchetypes() {
  const allArchetypes = new Set()

  Object.values(ARCHETYPES_BY_FORMAT).forEach(archetypes => {
    archetypes.forEach(archetype => allArchetypes.add(archetype))
  })

  return Array.from(allArchetypes).sort()
}
