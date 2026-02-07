export type Appointment = {
  id: number;
  patient_id: number;
  provider_id: number;
  service_name: string;
  start_time: string;
  end_time: string;
  status: string;
};

export type Patient = {
  id: number;
  full_name: string;
  email: string;
  phone: string;
};

export type InventoryItem = {
  id: number;
  name: string;
  sku: string;
  quantity: number;
  reorder_level: number;
};

export type ReportOverview = {
  total_appointments: number;
  total_revenue: number;
  paid_invoices: number;
};
