import { apiClient } from "./apiClient";
import type { DashboardData } from "../types/dashboard";

export async function getDashboardData(city: string): Promise<DashboardData> {
  const response = await apiClient.get<DashboardData>("/dashboard/", {
    params: {
      city,
    },
  });

  return response.data;
}
