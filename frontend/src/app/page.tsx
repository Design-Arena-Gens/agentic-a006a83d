'use client';

import { useState } from "react";
import { useTranslation } from "react-i18next";
import { DashboardView } from "@/components/views/dashboard-view";
import { PatientPortalView } from "@/components/views/patient-portal-view";
import { AdminPanelView } from "@/components/views/admin-panel-view";

const tabs = [
  { id: "dashboard", labelKey: "dashboard" },
  { id: "patient", labelKey: "patient_portal" },
  { id: "admin", labelKey: "admin_panel" },
];

export default function Home() {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState("dashboard");

  return (
    <div className="mx-auto flex min-h-screen max-w-6xl flex-col gap-8 px-4 py-10">
      <header className="space-y-3">
        <span className="inline-flex items-center rounded-full bg-brand-100 px-3 py-1 text-xs font-semibold text-brand-600">
          EsthetiManage
        </span>
        <h1 className="text-4xl font-bold text-slate-900 md:text-5xl">
          {t("welcome")}
        </h1>
        <p className="max-w-2xl text-base text-slate-600">
          {t("tagline")} Reduza no-shows, personalize jornadas e acompanhe métricas críticas em um único painel.
        </p>
        <nav className="flex gap-2">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`rounded-full px-4 py-2 text-sm font-semibold transition ${
                activeTab === tab.id
                  ? "bg-brand-500 text-white shadow"
                  : "bg-white text-slate-500 shadow-sm"
              }`}
            >
              {t(tab.labelKey)}
            </button>
          ))}
        </nav>
      </header>

      <main className="pb-10">
        {activeTab === "dashboard" && <DashboardView />}
        {activeTab === "patient" && <PatientPortalView />}
        {activeTab === "admin" && <AdminPanelView />}
      </main>
    </div>
  );
}
