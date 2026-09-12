import React, { useState, useEffect } from 'react';
import {
  LayoutDashboard,
  Calendar,
  User,
  Filter,
  Activity,
  ShieldCheck,
  Clock,
  Users,
  LogOut,
  ChevronsLeft,
  ChevronsRight
} from 'lucide-react';

import RequestForm from './components/RequestForm';
import ConflictCard from './components/ConflictCard';
import ExplanationReceipt from './components/ExplanationReceipt';
import GanttTimeline from './components/GanttTimeline';
import CorridorMap from './components/CorridorMap';
import Login from './components/login';
import ProfileModal from './components/Profilemodal';
import NotificationBell from './components/NotificationBell';

import {
  getDashboard,
  generatePlan,
  submitBlockRequest,
  getHistory
} from './api';

import { MAINTENANCE_BLOCKS } from './mockData';


export default function App() {

  // =========================================================
  // AUTH STATE
  // =========================================================

  const [user, setUser] = useState(null);
  const [showProfile, setShowProfile] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);


  // =========================================================
  // NOTIFICATIONS
  // =========================================================

  const [notifications, setNotifications] = useState([]);

  const addNotification = (title, message, type) => {
    const id = Date.now() + Math.random();

    setNotifications((prev) => [
      {
        id,
        title,
        message,
        type,
        read: false,
        time: new Date().toLocaleTimeString([], {
          hour: '2-digit',
          minute: '2-digit'
        })
      },
      ...prev
    ]);

    return id;
  };

  const markAllRead = () => {
    setNotifications((prev) =>
      prev.map((notification) => ({
        ...notification,
        read: true
      }))
    );
  };


  // =========================================================
  // BLOCK REQUEST
  // =========================================================

  const handleRequestSubmit = async (data) => {
    try {
      const response = await submitBlockRequest(data);

      addNotification(
        'Request sent',
        'Your manual block request was sent for review.',
        'sent'
      );

      addNotification(
        'Request processed',
        response?.message ||
          'Block request submitted successfully.',
        'approved'
      );

    } catch (error) {

      console.error('Block request failed:', error);

      addNotification(
        'Request failed',
        'Failed to submit block request.',
        'error'
      );
    }
  };


  // =========================================================
  // MAIN STATE
  // =========================================================

  const [activeTab, setActiveTab] = useState('dashboard');

  const [selectedBlockId, setSelectedBlockId] = useState(null);

  const [isResolved, setIsResolved] = useState(false);

  const [filterTask, setFilterTask] = useState('ALL');

  const [activeUsers, setActiveUsers] = useState(142);

  const [blocks, setBlocks] = useState([]);

  const [dashboardMetrics, setDashboardMetrics] = useState({
    active_blocks: 0,
    conflicts: 0,
    efficiency: 0,
    hours_saved: 0,
    optimizer_status: 'offline'
  });

  const [conflicts, setConflicts] = useState([]);

  const [isOptimizing, setIsOptimizing] = useState(false);

  const [explanationData, setExplanationData] = useState(null);

  const [historyData, setHistoryData] = useState([]);


  // =========================================================
  // SIMULATED LIVE USER COUNT
  // =========================================================

  useEffect(() => {

    const interval = setInterval(() => {

      setActiveUsers((previous) => {
        const change = Math.floor(Math.random() * 5) - 2;
        return Math.max(0, previous + change);
      });

    }, 5000);

    return () => clearInterval(interval);

  }, []);


  // =========================================================
  // FETCH DASHBOARD DATA
  // =========================================================

  const fetchData = async () => {

    try {

      const dashboard = await getDashboard();

      if (dashboard) {
        setDashboardMetrics((previous) => ({
          ...previous,
          ...dashboard
        }));
      }


      const history = await getHistory();

      setHistoryData(
        Array.isArray(history) ? history : []
      );


    } catch (error) {

      console.error('API failed:', error);

      setDashboardMetrics((previous) => ({
        ...previous,
        optimizer_status: 'offline/error'
      }));

    }

  };


  // =========================================================
  // LOAD DATA AFTER LOGIN
  // =========================================================

  useEffect(() => {

    if (user) {
      fetchData();
    }

  }, [user]);


  // =========================================================
  // AUTH GUARD
  // =========================================================

  if (!user) {

    return (
      <Login
        onLoginSuccess={(userData) => {
          setUser(userData);
        }}
      />
    );

  }


  // =========================================================
  // FILTERED BLOCKS
  // =========================================================

  const displayBlocks =
    filterTask === 'ALL'
      ? blocks
      : blocks.filter(
          (block) => block.id === filterTask
        );


  // =========================================================
  // CONFLICT CHECK
  // =========================================================

  const isConflict = conflicts.some(
    (conflict) =>
      conflict?.blockA?.id === selectedBlockId ||
      conflict?.blockB?.id === selectedBlockId
  );


  // =========================================================
  // SELECTED BLOCK
  // =========================================================

  const selectedBlockData = blocks.find(
    (block) => block.id === selectedBlockId
  );


  // =========================================================
  // AI OPTIMIZER
  // =========================================================

  const handleOptimize = async () => {

    setIsOptimizing(true);

    try {

      const result = await generatePlan({
        num_tasks: 10
      });


      const planBlocks =
        Array.isArray(result?.selected_candidates)
          ? result.selected_candidates
          : [];


      if (planBlocks.length === 0) {

        addNotification(
          'No schedule generated',
          'The optimizer did not return any feasible blocks.',
          'error'
        );

        return;
      }


      // -----------------------------------------------------
      // MAP BACKEND BLOCKS TO FRONTEND FORMAT
      // -----------------------------------------------------

      const mappedBlocks = planBlocks.map(
        (candidate, index) => {

          const startHour =
            Number(candidate?.start_hour) || 0;

          const duration =
            Number(candidate?.duration_hrs) || 1;

          const riskCovered =
            Number(candidate?.risk_covered) || 0;

          const urgency =
            Number(candidate?.urgency) || 0;

          return {
            id: `B-${String(index + 1).padStart(3, '0')}`,

            title:
              `Task ${candidate?.task_id ?? index + 1} Mega-block`,

            department: 'Engineering',

            sectionId:
              `SEC-${candidate?.section ?? 'N/A'}`,

            startHour,

            endHour: startHour + duration,

            status: 'Scheduled',

            type: 'Mega-Block',

            description:
              `Generated by OR-Tools. Risk covered: ${riskCovered.toFixed(2)}`,

            urgency
          };

        }
      );


      // -----------------------------------------------------
      // UPDATE UI
      // -----------------------------------------------------

      setBlocks(mappedBlocks);

      setConflicts([]);

      setSelectedBlockId(null);

      setIsResolved(false);


      // -----------------------------------------------------
      // EXPLANATION DATA
      // -----------------------------------------------------

      const taskNames = planBlocks
        .slice(0, 5)
        .map(
          (candidate) =>
            `Task ${candidate?.task_id ?? 'N/A'}`
        );


      setExplanationData({

        combinedTasks:
          taskNames.length > 0
            ? taskNames
            : ['Optimized maintenance tasks'],

        reasons: [
          'Tasks optimized by OR-Tools CP-SAT',
          'Low predicted train impact',
          'Safe resource allocation'
        ],

        hoursSaved:
          planBlocks.length * 1.5

      });


      // -----------------------------------------------------
      // REFRESH DASHBOARD / HISTORY
      // -----------------------------------------------------

      await fetchData();


      addNotification(
        'Schedule generated',
        `${planBlocks.length} optimized block(s) generated successfully.`,
        'approved'
      );


    } catch (error) {

      console.error(
        'Optimization failed:',
        error
      );

      addNotification(
        'Optimization failed',
        error?.message ||
          'Failed to generate plan. Ensure backend is running.',
        'error'
      );

    } finally {

      setIsOptimizing(false);

    }

  };


  // =========================================================
  // MAIN APPLICATION
  // =========================================================

  return (

    <div className="flex h-screen bg-slate-50 font-sans overflow-hidden text-slate-800">


      {/* =====================================================
          SIDEBAR
      ====================================================== */}

      <div
        className={`
          ${
            sidebarCollapsed
              ? 'w-20'
              : 'w-64'
          }
          bg-slate-900
          text-slate-300
          flex
          flex-col
          shadow-2xl
          z-20
          border-r
          border-slate-800
          shrink-0
          transition-all
          duration-200
        `}
      >


        {/* BRAND */}

        <div
          className="
            p-6
            border-b
            border-slate-800
            bg-slate-900/50
            flex
            items-center
            justify-between
          "
        >

          {sidebarCollapsed ? (

            <Activity
              className="text-blue-500 mx-auto"
              size={24}
            />

          ) : (

            <div>

              <h1
                className="
                  text-2xl
                  font-black
                  tracking-wider
                  text-white
                  flex
                  items-center
                  gap-2
                "
              >

                <Activity
                  className="text-blue-500"
                  size={24}
                />

                RailGrid

              </h1>

              <p
                className="
                  text-blue-400/80
                  text-[15px]
                  font-bold
                  uppercase
                  tracking-widest
                  mt-1.5
                "
              >
                AI Block Planning System
              </p>

            </div>

          )}

        </div>


        {/* COLLAPSE BUTTON */}

        <button
          onClick={() =>
            setSidebarCollapsed(
              (value) => !value
            )
          }
          title={
            sidebarCollapsed
              ? 'Expand sidebar'
              : 'Collapse sidebar'
          }
          className="
            mx-4
            mt-3
            flex
            items-center
            justify-center
            gap-2
            text-slate-500
            hover:text-white
            hover:bg-slate-800
            rounded-md
            py-1.5
            transition-colors
          "
        >

          {sidebarCollapsed ? (
            <ChevronsRight size={16} />
          ) : (
            <ChevronsLeft size={16} />
          )}

        </button>


        {/* NAVIGATION */}

        <nav
          className="
            flex-1
            p-4
            space-y-1.5
            mt-2
          "
        >

          {/* DASHBOARD */}

          <button
            onClick={() =>
              setActiveTab('dashboard')
            }
            title="Live Dashboard"
            className={`
              w-full
              flex
              items-center
              ${
                sidebarCollapsed
                  ? 'justify-center'
                  : 'space-x-3'
              }
              px-4
              py-3
              rounded-md
              transition-all
              duration-200
              ${
                activeTab === 'dashboard'
                  ? 'bg-blue-700 text-white shadow-md'
                  : 'hover:bg-slate-800 hover:text-white'
              }
            `}
          >

            <LayoutDashboard size={18} />

            {!sidebarCollapsed && (
              <span
                className="
                  font-semibold
                  text-sm
                "
              >
                Live Dashboard
              </span>
            )}

          </button>


          {/* HISTORY */}

          <button
            onClick={() =>
              setActiveTab('history')
            }
            title="Schedule History"
            className={`
              w-full
              flex
              items-center
              ${
                sidebarCollapsed
                  ? 'justify-center'
                  : 'space-x-3'
              }
              px-4
              py-3
              rounded-md
              transition-all
              duration-200
              ${
                activeTab === 'history'
                  ? 'bg-blue-700 text-white shadow-md'
                  : 'hover:bg-slate-800 hover:text-white'
              }
            `}
          >

            <Calendar size={18} />

            {!sidebarCollapsed && (
              <span
                className="
                  font-semibold
                  text-sm
                "
              >
                Schedule History
              </span>
            )}

          </button>

        </nav>


        {/* USER AREA */}

        <div
          className={`
            p-5
            border-t
            border-slate-800
            bg-slate-950/30
            flex
            items-center
            ${
              sidebarCollapsed
                ? 'justify-center'
                : 'justify-between'
            }
          `}
        >

          <button
            onClick={() =>
              setShowProfile(true)
            }
            title={user?.username}
            className={`
              flex
              items-center
              ${
                sidebarCollapsed
                  ? ''
                  : 'space-x-3'
              }
              min-w-0
              hover:bg-slate-800/60
              rounded-md
              -m-1.5
              p-1.5
              transition-colors
              text-left
            `}
          >

            <div
              className="
                bg-slate-800
                p-2
                rounded-md
                text-blue-400
                shrink-0
              "
            >
              <User size={16} />
            </div>


            {!sidebarCollapsed && (

              <div className="min-w-0">

                <p
                  className="
                    text-slate-500
                    text-[9px]
                    uppercase
                    font-bold
                    tracking-wider
                  "
                >
                  {user?.role || 'User'}
                </p>

                <p
                  className="
                    font-bold
                    text-slate-200
                    text-xs
                    truncate
                  "
                >
                  {user?.username || 'Operator'}
                </p>

              </div>

            )}

          </button>


          {!sidebarCollapsed && (

            <button
              onClick={() => {
                setShowProfile(false);
                setUser(null);
              }}
              title="Log out"
              className="
                text-slate-500
                hover:text-red-400
                transition-colors
                shrink-0
                ml-2
              "
            >
              <LogOut size={16} />
            </button>

          )}

        </div>

      </div>


      {/* =====================================================
          PROFILE MODAL
      ====================================================== */}

      {showProfile && (

        <ProfileModal
          user={user}
          onClose={() =>
            setShowProfile(false)
          }
          onLogout={() => {
            setShowProfile(false);
            setUser(null);
          }}
        />

      )}


      {/* =====================================================
          MAIN CONTENT
      ====================================================== */}

      <div
        className="
          flex-1
          flex
          flex-col
          overflow-auto
          z-10
          relative
        "
      >


        {/* ===================================================
            TOP HEADER
        ==================================================== */}

        <header
          className="
            bg-white
            shadow-sm
            px-8
            py-4
            flex
            justify-between
            items-center
            sticky
            top-0
            z-20
            border-b
            border-slate-200
            shrink-0
          "
        >

          <div>

            <h2
              className="
                text-lg
                font-bold
                text-slate-800
              "
            >
              Divisional Overview
            </h2>

            <p
              className="
                text-xs
                text-slate-500
                font-medium
              "
            >
              Mumbai Railway Network
            </p>

          </div>


          <div
            className="
              flex
              space-x-5
              items-center
            "
          >

            {/* ACTIVE USERS */}

            <div
              className="
                flex
                items-center
                space-x-2
                bg-slate-100
                px-3
                py-1.5
                rounded-md
                border
                border-slate-200
                shadow-sm
                transition-all
                duration-300
              "
            >

              <Users
                size={14}
                className="text-blue-600"
              />

              <span
                className="
                  text-[11px]
                  font-bold
                  text-slate-600
                  uppercase
                  tracking-wide
                "
              >

                <span
                  className="
                    text-blue-700
                    font-black
                  "
                >
                  {activeUsers}
                </span>

                {' '}Active

              </span>

            </div>


            {/* NOTIFICATIONS */}

            <NotificationBell
              notifications={notifications}
              onOpen={markAllRead}
            />


            {/* OPTIMIZER STATUS */}

            <div
              className="
                flex
                items-center
                space-x-2
                bg-teal-50
                px-3
                py-1.5
                rounded-md
                border
                border-teal-200
                shadow-sm
              "
            >

              <span
                className="
                  w-2
                  h-2
                  bg-teal-600
                  rounded-full
                  animate-pulse
                "
              />

              <span
                className="
                  text-[11px]
                  font-bold
                  text-teal-800
                  uppercase
                  tracking-wide
                "
              >
                Optimizer Online
              </span>

            </div>

          </div>

        </header>


        {/* ===================================================
            HISTORY PAGE
        ==================================================== */}

        {activeTab === 'history' ? (

          <div
            className="
              flex-1
              flex
              flex-col
              items-center
              justify-start
              p-8
              overflow-y-auto
              animate-in
              fade-in
              duration-300
            "
          >

            <div
              className="
                w-full
                max-w-4xl
                flex
                justify-between
                items-center
                mb-6
              "
            >

              <h2
                className="
                  text-2xl
                  font-bold
                  text-slate-800
                  flex
                  items-center
                  gap-2
                "
              >

                <Calendar
                  size={24}
                  className="text-blue-600"
                />

                Schedule History

              </h2>


              <button
                onClick={handleOptimize}
                disabled={isOptimizing}
                className={`
                  px-4
                  py-2
                  rounded-md
                  font-semibold
                  text-sm
                  shadow-sm
                  transition-colors
                  ${
                    isOptimizing
                      ? 'bg-slate-300 text-slate-500 cursor-not-allowed'
                      : 'bg-blue-600 text-white hover:bg-blue-700'
                  }
                `}
              >

                {isOptimizing
                  ? 'Generating...'
                  : 'Generate New Schedule'}

              </button>

            </div>


            {historyData.length === 0 ? (

              <div
                className="
                  flex
                  flex-col
                  items-center
                  justify-center
                  mt-20
                  opacity-60
                "
              >

                <Calendar
                  size={48}
                  className="text-slate-300 mb-4"
                />

                <p
                  className="
                    text-sm
                    text-slate-500
                    mt-2
                  "
                >
                  No schedules generated yet.
                </p>

              </div>

            ) : (

              <div
                className="
                  w-full
                  max-w-4xl
                  space-y-4
                "
              >

                {historyData.map(
                  (historyItem, index) => (

                    <div
                      key={
                        historyItem?.timestamp ||
                        index
                      }
                      className="
                        bg-white
                        border
                        border-slate-200
                        rounded-lg
                        p-5
                        shadow-sm
                        flex
                        flex-col
                        md:flex-row
                        md:items-center
                        justify-between
                        gap-4
                        transition-all
                        hover:shadow-md
                      "
                    >

                      <div>

                        <p
                          className="
                            text-xs
                            font-bold
                            text-slate-400
                            uppercase
                            tracking-widest
                            mb-1
                          "
                        >
                          Generated{' '}
                          {historyItem?.timestamp
                            ? new Date(
                                historyItem.timestamp
                              ).toLocaleString()
                            : 'Recently'}
                        </p>


                        <h3
                          className="
                            text-lg
                            font-black
                            text-slate-700
                          "
                        >
                          Plan #{historyData.length - index}
                        </h3>


                        <div
                          className="
                            flex
                            gap-3
                            mt-2
                          "
                        >

                          <span
                            className={`
                              text-xs
                              font-bold
                              px-2
                              py-1
                              rounded-md
                              ${
                                historyItem?.status ===
                                'FEASIBLE'
                                  ? 'bg-teal-100 text-teal-800'
                                  : 'bg-blue-100 text-blue-800'
                              }
                            `}
                          >
                            Status:{' '}
                            {historyItem?.status ||
                              'Generated'}
                          </span>


                          <span
                            className="
                              text-xs
                              font-bold
                              px-2
                              py-1
                              rounded-md
                              bg-slate-100
                              text-slate-700
                            "
                          >
                            {historyItem?.blocks_generated ||
                              0}{' '}
                            Blocks
                          </span>

                        </div>

                      </div>


                      <button
                        onClick={() =>
                          setActiveTab(
                            'dashboard'
                          )
                        }
                        className="
                          text-sm
                          font-semibold
                          text-blue-600
                          hover:text-blue-800
                          bg-blue-50
                          hover:bg-blue-100
                          px-4
                          py-2
                          rounded-md
                          transition-colors
                        "
                      >
                        View on Dashboard
                      </button>

                    </div>

                  )
                )}

              </div>

            )}

          </div>

        ) : (

          /* =================================================
             DASHBOARD
          ================================================== */

          <main
            className="
              p-6
              flex-1
              flex
              flex-col
              space-y-5
              overflow-y-auto
            "
          >


            {/* =================================================
                KPI RIBBON
            ================================================== */}

            <div
              className="
                grid
                grid-cols-1
                md:grid-cols-4
                gap-4
                mb-1
                shrink-0
              "
            >

              {/* ACTIVE BLOCKS */}

              <div
                className="
                  bg-white
                  p-4
                  rounded-lg
                  shadow-sm
                  border
                  border-slate-200
                  flex
                  items-center
                  space-x-4
                  border-l-4
                  border-l-blue-500
                "
              >

                <div
                  className="
                    bg-slate-50
                    p-2.5
                    rounded
                    text-blue-600
                  "
                >
                  <LayoutDashboard size={20} />
                </div>

                <div>

                  <p
                    className="
                      text-[10px]
                      font-bold
                      text-slate-500
                      uppercase
                    "
                  >
                    Active Blocks
                  </p>

                  <h4
                    className="
                      text-lg
                      font-black
                      text-slate-800
                    "
                  >
                    {dashboardMetrics.active_blocks ?? 0}
                  </h4>

                </div>

              </div>


              {/* CONFLICTS */}

              <div
                className="
                  bg-white
                  p-4
                  rounded-lg
                  shadow-sm
                  border
                  border-slate-200
                  flex
                  items-center
                  space-x-4
                  border-l-4
                  border-l-red-500
                "
              >

                <div
                  className="
                    bg-slate-50
                    p-2.5
                    rounded
                    text-red-600
                  "
                >
                  <ShieldCheck size={20} />
                </div>

                <div>

                  <p
                    className="
                      text-[10px]
                      font-bold
                      text-slate-500
                      uppercase
                    "
                  >
                    Conflicts Detected
                  </p>

                  <h4
                    className="
                      text-lg
                      font-black
                      text-slate-800
                    "
                  >
                    {dashboardMetrics.conflicts ?? 0}
                  </h4>

                </div>

              </div>


              {/* EFFICIENCY */}

              <div
                className="
                  bg-white
                  p-4
                  rounded-lg
                  shadow-sm
                  border
                  border-slate-200
                  flex
                  items-center
                  space-x-4
                  border-l-4
                  border-l-teal-500
                "
              >

                <div
                  className="
                    bg-slate-50
                    p-2.5
                    rounded
                    text-teal-600
                  "
                >
                  <Activity size={20} />
                </div>

                <div>

                  <p
                    className="
                      text-[10px]
                      font-bold
                      text-slate-500
                      uppercase
                    "
                  >
                    AI Efficiency
                  </p>

                  <h4
                    className="
                      text-lg
                      font-black
                      text-slate-800
                    "
                  >
                    {dashboardMetrics.efficiency ?? 0}%
                  </h4>

                </div>

              </div>


              {/* HOURS SAVED */}

              <div
                className="
                  bg-white
                  p-4
                  rounded-lg
                  shadow-sm
                  border
                  border-slate-200
                  flex
                  items-center
                  space-x-4
                  border-l-4
                  border-l-slate-700
                "
              >

                <div
                  className="
                    bg-slate-50
                    p-2.5
                    rounded
                    text-slate-700
                  "
                >
                  <Clock size={20} />
                </div>

                <div>

                  <p
                    className="
                      text-[10px]
                      font-bold
                      text-slate-500
                      uppercase
                    "
                  >
                    Hours Saved
                  </p>

                  <h4
                    className="
                      text-lg
                      font-black
                      text-slate-800
                    "
                  >
                    {dashboardMetrics.hours_saved ?? 0} hrs
                  </h4>

                </div>

              </div>

            </div>


            {/* =================================================
                FILTER TOOLBAR
            ================================================== */}

            <div
              className="
                bg-white
                px-5
                py-2.5
                rounded-lg
                shadow-sm
                border
                border-slate-200
                flex
                justify-between
                items-center
                z-10
                shrink-0
              "
            >

              <div
                className="
                  flex
                  items-center
                  space-x-2
                  text-slate-700
                "
              >

                <Filter size={16} />

                <span
                  className="
                    text-xs
                    font-bold
                    uppercase
                    tracking-wide
                  "
                >
                  Data Filter
                </span>

              </div>


              <select
                value={filterTask}
                onChange={(event) =>
                  setFilterTask(
                    event.target.value
                  )
                }
                className="
                  bg-slate-50
                  border
                  border-slate-200
                  text-slate-700
                  text-xs
                  font-medium
                  rounded-md
                  focus:ring-blue-600
                  focus:border-blue-600
                  block
                  p-2
                  cursor-pointer
                  outline-none
                "
              >

                <option value="ALL">
                  Show All Scheduled Tasks
                </option>

                {MAINTENANCE_BLOCKS.map(
                  (block) => (

                    <option
                      key={block.id}
                      value={block.id}
                    >
                      {block.id}: {block.title} (
                      {block.department})
                    </option>

                  )
                )}

              </select>

            </div>


            {/* =================================================
                GANTT + MAP
            ================================================== */}

            <div
              className="
                grid
                grid-cols-1
                lg:grid-cols-2
                gap-5
                h-[450px]
                shrink-0
              "
            >

              {/* GANTT */}

              <div
                className="
                  bg-white
                  rounded-lg
                  shadow-sm
                  border
                  border-slate-200
                  overflow-hidden
                  transition-all
                  duration-300
                  h-full
                "
              >

                <GanttTimeline
                  selectedBlockId={
                    selectedBlockId
                  }
                  onSelectBlock={
                    setSelectedBlockId
                  }
                  filteredBlocks={
                    displayBlocks
                  }
                  conflicts={conflicts}
                />

              </div>


              {/* MAP */}

              <div
                className="
                  bg-white
                  rounded-lg
                  shadow-sm
                  border
                  border-slate-200
                  p-1
                  transition-all
                  duration-300
                  h-full
                "
              >

                <CorridorMap
                  selectedBlockId={
                    selectedBlockId
                  }
                  onSelectBlock={
                    setSelectedBlockId
                  }
                  filteredBlocks={
                    displayBlocks
                  }
                />

              </div>

            </div>


            {/* =================================================
                REQUEST + DIAGNOSTIC
            ================================================== */}

            <div
              className="
                grid
                grid-cols-1
                lg:grid-cols-3
                gap-5
                pb-8
                min-h-[420px]
                shrink-0
                items-stretch
              "
            >

              {/* REQUEST FORM */}

              <div
                className="
                  lg:col-span-1
                  h-full
                "
              >

                <RequestForm
                  onSubmit={
                    handleRequestSubmit
                  }
                />

              </div>


              {/* DIAGNOSTIC ENGINE */}

              <div
                className="
                  lg:col-span-2
                  bg-slate-100/50
                  rounded-lg
                  shadow-inner
                  border
                  border-slate-200
                  p-6
                  flex
                  flex-col
                  justify-center
                  items-center
                  relative
                  overflow-hidden
                  h-full
                "
              >

                <h3
                  className="
                    absolute
                    top-4
                    left-5
                    text-[10px]
                    font-bold
                    text-slate-400
                    uppercase
                    tracking-widest
                  "
                >
                  Diagnostic Engine
                </h3>


                <div
                  className="
                    w-full
                    max-w-lg
                    mt-4
                    transition-all
                    duration-500
                    ease-in-out
                  "
                >


                  {/* NOTHING SELECTED */}

                  {!selectedBlockId && (

                    <div
                      className="
                        text-center
                        py-10
                        opacity-60
                      "
                    >

                      <LayoutDashboard
                        size={40}
                        className="
                          mx-auto
                          text-slate-400
                          mb-3
                        "
                      />

                      <p
                        className="
                          text-slate-500
                          text-sm
                          font-medium
                        "
                      >
                        Select a block on the
                        timeline or map to run
                        diagnostics.
                      </p>

                    </div>

                  )}


                  {/* CONFLICT */}

                  {selectedBlockId &&
                    isConflict &&
                    !isResolved && (

                      <div
                        className="
                          animate-in
                          fade-in
                          slide-in-from-bottom-4
                          duration-500
                        "
                      >

                        <ConflictCard
                          conflictData={{
                            severity:
                              'critical',

                            type:
                              'Unsafe Track Overlap',

                            description:
                              `Critical resource and spatial conflict detected at ${
                                selectedBlockData?.sectionId ||
                                'selected section'
                              }.`,
                            
                            departments: [
                              'Track',
                              'Civil'
                            ],

                            overlapTime:
                              `${selectedBlockData?.startHour ?? 0}:00 - ${
                                selectedBlockData?.endHour ?? 0
                              }:00`
                          }}

                          onRunOptimizer={
                            handleOptimize
                          }

                          isOptimizing={
                            isOptimizing
                          }
                        />

                      </div>

                  )}


                  {/* RESOLVED */}

                  {selectedBlockId &&
                    isResolved &&
                    explanationData && (

                      <div
                        className="
                          animate-in
                          fade-in
                          zoom-in-95
                          duration-500
                        "
                      >

                        <ExplanationReceipt
                          explanationData={
                            explanationData
                          }
                        />

                      </div>

                  )}


                  {/* SAFE */}

                  {selectedBlockId &&
                    !isConflict &&
                    !isResolved && (

                      <div
                        className="
                          bg-white
                          border-l-4
                          border-l-teal-500
                          shadow-sm
                          p-5
                          rounded-r-md
                          text-left
                          mt-6
                          animate-in
                          fade-in
                          slide-in-from-bottom-4
                          duration-500
                          flex
                          items-center
                          space-x-4
                        "
                      >

                        <div
                          className="
                            bg-teal-50
                            p-3
                            rounded-full
                          "
                        >

                          <ShieldCheck
                            size={28}
                            className="
                              text-teal-600
                            "
                          />

                        </div>


                        <div>

                          <h4
                            className="
                              text-slate-800
                              font-black
                              text-base
                            "
                          >
                            Safe Track Block Verified
                          </h4>

                          <p
                            className="
                              text-slate-500
                              font-medium
                              text-xs
                              mt-0.5
                            "
                          >
                            Block {selectedBlockId}
                            {' '}has no conflicts
                            and is cleared for
                            execution.
                          </p>

                        </div>

                      </div>

                  )}

                </div>

              </div>

            </div>

          </main>

        )}

      </div>

    </div>

  );

}
