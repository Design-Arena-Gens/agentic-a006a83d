'use client';

import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import dayjs from "dayjs";
import { getAppointments, getInventory, getOverview } from "@/services/api";

export function AdminPanelView() {
  const { data: overview } = useQuery({
    queryKey: ["overview"],
    queryFn: getOverview,
  });
  const { data: inventory = [] } = useQuery({
    queryKey: ["inventory"],
    queryFn: getInventory,
  });
  const { data: appointments = [] } = useQuery({
    queryKey: ["appointments"],
    queryFn: getAppointments,
  });

  const occupancy = useMemo(() => {
    const totalSlots = 40;
    const booked = appointments.length;
    return Math.min(100, Math.round((booked / totalSlots) * 100));
  }, [appointments]);

  return (
    <div className="space-y-6">
      <div className="grid gap-6 md:grid-cols-3">
        <div className="card">
          <p className="text-sm text-slate-500">Receita projetada</p>
          <p className="mt-2 text-2xl font-semibold text-slate-900">
            R$ {(overview?.total_revenue ?? 0).toLocaleString("pt-BR", { minimumFractionDigits: 2 })}
          </p>
          <p className="text-xs text-slate-400">Inclui pagamentos Stripe confirmados</p>
        </div>
        <div className="card">
          <p className="text-sm text-slate-500">Taxa de ocupação</p>
          <p className="mt-2 text-2xl font-semibold text-slate-900">{occupancy}%</p>
          <p className="text-xs text-slate-400">
            Considerando 40 slots semanais
          </p>
        </div>
        <div className="card">
          <p className="text-sm text-slate-500">Integrações</p>
          <ul className="mt-2 space-y-1 text-sm text-slate-600">
            <li>✅ Stripe pagamentos</li>
            <li>✅ Twilio SMS lembretes</li>
            <li>⚠️ Google Calendar aguardando credenciais</li>
          </ul>
        </div>
      </div>

      <div className="card">
        <h3 className="section-title mb-4">Estoque crítico</h3>
        <div className="overflow-hidden rounded-xl border border-slate-100">
          <table className="min-w-full divide-y divide-slate-100 text-sm">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-4 py-2 text-left font-medium text-slate-600">Produto</th>
                <th className="px-4 py-2 text-left font-medium text-slate-600">SKU</th>
                <th className="px-4 py-2 text-left font-medium text-slate-600">Qtd.</th>
                <th className="px-4 py-2 text-left font-medium text-slate-600">Reposição</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {inventory.map((item) => {
                const isLow = item.quantity <= item.reorder_level;
                return (
                  <tr key={item.id} className={isLow ? "bg-amber-50" : ""}>
                    <td className="px-4 py-2">{item.name}</td>
                    <td className="px-4 py-2 font-mono text-xs text-slate-500">{item.sku}</td>
                    <td className="px-4 py-2">{item.quantity}</td>
                    <td className="px-4 py-2">{item.reorder_level}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      <div className="card">
        <h3 className="section-title mb-4">Atividades recentes</h3>
        <ul className="space-y-2 text-sm text-slate-600">
          {appointments.slice(0, 4).map((appointment) => (
            <li key={appointment.id} className="flex items-center justify-between">
              <span>{appointment.service_name}</span>
              <span className="text-xs text-slate-500">
                {dayjs(appointment.start_time).format("DD/MM/YYYY HH:mm")}
              </span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
