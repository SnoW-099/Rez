// api.js - API functions to communicate with the backend

import axios from "axios";
import { API_CONFIG } from "./config";

// Configure axios instance with base URL
const api = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: 8000,
});

// Get bot status
export const getBotStatus = async () => {
  try {
    const response = await api.get("/status");
    return response.data;
  } catch (error) {
    console.error("Error getting bot status:", error);
    throw error;
  }
};

// Get bot statistics
export const getBotStats = async () => {
  try {
    const response = await api.get("/stats");
    return response.data;
  } catch (error) {
    console.error("Error getting bot stats:", error);
    throw error;
  }
};

// Get command list from API
export const getCommands = async () => {
  try {
    const response = await api.get("/commands");
    return response.data;
  } catch (error) {
    console.error("Error getting commands:", error);
    // Fallback with all current commands
    return [
      // Utility
      {
        name: "!help",
        description: "Shows all commands",
        category: "Utility",
        role: "user",
      },
      {
        name: "!ping",
        description: "Check bot latency",
        category: "Utility",
        role: "user",
      },

      // Economy
      {
        name: "!profile [@user]",
        description: "Your complete profile",
        category: "Economy",
        role: "user",
      },
      {
        name: "!balance [@user]",
        description: "Check your balance",
        category: "Economy",
        role: "user",
      },
      {
        name: "!work",
        description: "Work and earn $50-200 (3min cd)",
        category: "Economy",
        role: "user",
      },
      {
        name: "!daily",
        description: "Daily reward $200-500",
        category: "Economy",
        role: "user",
      },
      {
        name: "!transfer @user $",
        description: "Transfer money",
        category: "Economy",
        role: "user",
      },
      {
        name: "!rob @user",
        description: "Rob (50% success)",
        category: "Economy",
        role: "user",
      },
      {
        name: "!ranking",
        description: "Top 5 richest",
        category: "Economy",
        role: "user",
      },
      {
        name: "!shop",
        description: "Item shop",
        category: "Economy",
        role: "user",
      },
      {
        name: "!buy [item]",
        description: "Buy an item",
        category: "Economy",
        role: "user",
      },

      // Levels
      {
        name: "!level [@user]",
        description: "View level and XP",
        category: "Levels",
        role: "user",
      },
      {
        name: "!leaderboard",
        description: "Top 10 by XP",
        category: "Levels",
        role: "user",
      },

      // Casino
      {
        name: "!coinflip $ heads/tails",
        description: "Bet heads or tails",
        category: "Casino",
        role: "user",
      },
      {
        name: "!slots $",
        description: "Slot machine",
        category: "Casino",
        role: "user",
      },
      {
        name: "!blackjack $",
        description: "Play 21",
        category: "Casino",
        role: "user",
      },
      {
        name: "!roulette $ color/num",
        description: "Casino roulette",
        category: "Casino",
        role: "user",
      },

      // Giveaways
      {
        name: "!giveaway [time] [prize]",
        description: "Create giveaway",
        category: "Giveaways",
        role: "admin",
      },
      {
        name: "!gend",
        description: "End giveaway",
        category: "Giveaways",
        role: "admin",
      },
      {
        name: "!greroll [id]",
        description: "Reroll winner",
        category: "Giveaways",
        role: "admin",
      },

      // Tickets
      {
        name: "!ticket [reason]",
        description: "Create support ticket",
        category: "Tickets",
        role: "user",
      },
      {
        name: "!close",
        description: "Close current ticket",
        category: "Tickets",
        role: "user",
      },

      // Moderation
      {
        name: "!warn @user",
        description: "Warn (3 = kick)",
        category: "Moderation",
        role: "admin",
      },
      {
        name: "!mute @user [time]",
        description: "Mute user",
        category: "Moderation",
        role: "admin",
      },
      {
        name: "!kick @user",
        description: "Kick from server",
        category: "Moderation",
        role: "admin",
      },
      {
        name: "!ban @user",
        description: "Permanent ban",
        category: "Moderation",
        role: "admin",
      },
      {
        name: "!clear [1-100]",
        description: "Delete messages",
        category: "Moderation",
        role: "admin",
      },
      {
        name: "!slowmode [sec]",
        description: "Slowmode",
        category: "Moderation",
        role: "admin",
      },

      // Owner
      {
        name: "!addmoney @user $",
        description: "Give money to user",
        category: "Owner",
        role: "owner",
      },
      {
        name: "!removemoney @user $",
        description: "Remove money from user",
        category: "Owner",
        role: "owner",
      },
      {
        name: "!setbalance @user $",
        description: "Set exact balance",
        category: "Owner",
        role: "owner",
      },
      {
        name: "!setlevel @user level",
        description: "Set user level",
        category: "Owner",
        role: "owner",
      },
      {
        name: "!resetuser @user",
        description: "Reset all data",
        category: "Owner",
        role: "owner",
      },
      {
        name: "!botstat",
        description: "Detailed bot statistics",
        category: "Owner",
        role: "owner",
      },
    ];
  }
};

// Get bank data
export const getBankData = async () => {
  try {
    const response = await api.get("/bank-data");
    return response.data;
  } catch (error) {
    console.error("Error getting bank data:", error);
    return {
      totalUsers: 0,
      totalCoins: 0,
      averageBalance: 0,
      topUsers: [],
    };
  }
};

const apiMethods = {
  getBotStatus,
  getBotStats,
  getCommands,
  getBankData,
};

export default apiMethods;
