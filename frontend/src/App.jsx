import { useEffect, useRef, useState } from "react";
import axios from "axios";

import {
  Activity,
  AlertCircle,
  BarChart3,
  Brain,
  ChevronRight,
  CircleAlert,
  FileImage,
  FileText,
  Leaf,
  Loader2,
  MapPin,
  RefreshCw,
  Recycle,
  ShieldCheck,
  Sparkles,
  Trash2,
  Upload,
  X,
} from "lucide-react";

import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  // =========================================================
  // FILE / ANALYSIS
  // =========================================================

  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [result, setResult] = useState(null);

  const [analyzing, setAnalyzing] = useState(false);
  const [uploadError, setUploadError] = useState("");

  // =========================================================
  // CITY / LOCAL GUIDANCE
  // =========================================================

  const [city, setCity] = useState("Indore");
  const [localGuidance, setLocalGuidance] = useState(null);
  const [localLoading, setLocalLoading] = useState(false);
  const [localError, setLocalError] = useState("");

  // =========================================================
  // DASHBOARD
  // =========================================================

  const [history, setHistory] = useState([]);

  const [stats, setStats] = useState({
    total_scans: 0,
    recyclable_scans: 0,
    non_recyclable_scans: 0,
    average_confidence: 0,
  });

  const [dashboardLoading, setDashboardLoading] =
    useState(false);

  // =========================================================
  // INDIVIDUAL HISTORY CITY
  // =========================================================

  /*
   * Stores the selected city separately for every
   * history scan.
   *
   * Example:
   * {
   *   24: "Bhopal",
   *   23: "Delhi",
   *   22: "Mumbai"
   * }
   */
  const [historyCities, setHistoryCities] =
    useState({});

  // =========================================================
  // DELETE
  // =========================================================

  const [deletingScanId, setDeletingScanId] =
    useState(null);

  const [deletingAll, setDeletingAll] =
    useState(false);

  // =========================================================
  // REPORT
  // =========================================================

  const [generatingReportId, setGeneratingReportId] =
    useState(null);

  // =========================================================
  // REFS
  // =========================================================

  const fileInputRef = useRef(null);
  const analysisResultRef = useRef(null);

  // =========================================================
  // LOAD DASHBOARD DATA
  // =========================================================

  const loadDashboardData = async () => {
    setDashboardLoading(true);

    try {
      const [
        historyResponse,
        statsResponse,
      ] = await Promise.all([
        axios.get(`${API_URL}/api/history`),
        axios.get(`${API_URL}/api/stats`),
      ]);

      const scans =
        historyResponse.data?.scans;

      setHistory(
        Array.isArray(scans)
          ? scans
          : []
      );

      const backendStats =
        statsResponse.data?.stats;

      setStats(
        backendStats || {
          total_scans: 0,
          recyclable_scans: 0,
          non_recyclable_scans: 0,
          average_confidence: 0,
        }
      );
    } catch (error) {
      console.error(
        "Dashboard loading error:",
        error
      );

      setHistory([]);

      setStats({
        total_scans: 0,
        recyclable_scans: 0,
        non_recyclable_scans: 0,
        average_confidence: 0,
      });
    } finally {
      setDashboardLoading(false);
    }
  };

  // =========================================================
  // INITIAL LOAD
  // =========================================================

  useEffect(() => {
    loadDashboardData();
  }, []);

  // =========================================================
  // IMAGE URL
  // =========================================================

  const getImageUrl = (imageUrl) => {
    if (!imageUrl) {
      return "";
    }

    if (
      imageUrl.startsWith("http://") ||
      imageUrl.startsWith("https://") ||
      imageUrl.startsWith("blob:")
    ) {
      return imageUrl;
    }

    return `${API_URL}${imageUrl}`;
  };

  // =========================================================
  // FILE SELECTION
  // =========================================================

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    setUploadError("");
    setResult(null);
    setLocalGuidance(null);
    setLocalError("");

    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }

    const newPreviewUrl =
      URL.createObjectURL(file);

    setSelectedFile(file);
    setPreviewUrl(newPreviewUrl);
  };

  // =========================================================
  // REMOVE IMAGE
  // =========================================================

  const handleRemoveImage = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }

    setSelectedFile(null);
    setPreviewUrl("");
    setResult(null);
    setLocalGuidance(null);
    setLocalError("");
    setUploadError("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  // =========================================================
  // CHANGE IMAGE
  // =========================================================

  const handleChangeImage = () => {
    fileInputRef.current?.click();
  };

  // =========================================================
  // ANALYZE IMAGE
  // =========================================================

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setUploadError(
        "Please select an image before analyzing."
      );
      return;
    }

    setAnalyzing(true);
    setUploadError("");
    setResult(null);
    setLocalGuidance(null);
    setLocalError("");

    try {
      const formData = new FormData();

      formData.append(
        "file",
        selectedFile
      );

      const response = await axios.post(
        `${API_URL}/api/analyze`,
        formData,
        {
          headers: {
            "Content-Type":
              "multipart/form-data",
          },
        }
      );

      if (
        response.data?.status === "error"
      ) {
        throw new Error(
          response.data.message ||
            "Analysis failed."
        );
      }

      setResult(response.data);

      await loadDashboardData();

      setTimeout(() => {
        analysisResultRef.current?.scrollIntoView(
          {
            behavior: "smooth",
            block: "start",
          }
        );
      }, 300);
    } catch (error) {
      console.error(
        "Analysis error:",
        error
      );

      const message =
        error.response?.data?.detail ||
        error.response?.data?.message ||
        error.message ||
        "Unable to analyze the image.";

      setUploadError(message);
    } finally {
      setAnalyzing(false);
    }
  };

  // =========================================================
  // LOCAL DISPOSAL GUIDANCE
  // =========================================================

  const loadLocalGuidance = async (
    category,
    selectedCity
  ) => {
    if (!category) {
      setLocalGuidance(null);
      return;
    }

    setLocalLoading(true);
    setLocalError("");

    try {
      const response = await axios.get(
        `${API_URL}/api/local-disposal`,
        {
          params: {
            category,
            city: selectedCity,
          },
        }
      );

      if (
        response.data?.status === "error"
      ) {
        throw new Error(
          response.data.message ||
            "Unable to load local guidance."
        );
      }

      setLocalGuidance(
        response.data?.guidance || null
      );
    } catch (error) {
      console.error(
        "Local guidance error:",
        error
      );

      setLocalError(
        error.response?.data?.detail ||
          error.response?.data?.message ||
          error.message ||
          "Unable to load local disposal guidance."
      );

      setLocalGuidance(null);
    } finally {
      setLocalLoading(false);
    }
  };

  // =========================================================
  // LOAD LOCAL GUIDANCE WHEN CITY / RESULT CHANGES
  // =========================================================

  useEffect(() => {
    const category =
      result?.analysis?.classification
        ?.category;

    if (!category) {
      setLocalGuidance(null);
      return;
    }

    loadLocalGuidance(
      category,
      city
    );
  }, [city, result]);

  // =========================================================
  // GENERATE PDF REPORT
  // =========================================================

  const generateReport = async (
    scanId,
    selectedCity = city
  ) => {
    if (!scanId) {
      alert(
        "Scan ID is missing. Please analyze the image again."
      );
      return;
    }

    setGeneratingReportId(scanId);

    try {
      const response = await axios.get(
        `${API_URL}/api/report/${scanId}`,
        {
          params: {
            city: selectedCity,
          },
          responseType: "blob",
        }
      );

      const contentType =
        response.headers?.[
          "content-type"
        ] || "";

      if (
        !contentType.includes(
          "application/pdf"
        )
      ) {
        try {
          const text =
            await response.data.text();

          const parsed =
            JSON.parse(text);

          throw new Error(
            parsed.detail ||
              parsed.message ||
              "Report generation failed."
          );
        } catch (parseError) {
          if (
            parseError instanceof Error &&
            parseError.message !==
              "Unexpected end of JSON input"
          ) {
            throw parseError;
          }

          throw new Error(
            "Report generation failed."
          );
        }
      }

      const pdfBlob = new Blob(
        [response.data],
        {
          type: "application/pdf",
        }
      );

      const downloadUrl =
        window.URL.createObjectURL(
          pdfBlob
        );

      const link =
        document.createElement("a");

      link.href = downloadUrl;

      link.download =
        `EcoVision_Report_${scanId}_${selectedCity}.pdf`;

      document.body.appendChild(link);

      link.click();

      document.body.removeChild(link);

      window.URL.revokeObjectURL(
        downloadUrl
      );
    } catch (error) {
      console.error(
        "Report generation error:",
        error
      );

      alert(
        error.message ||
          "Unable to generate the report."
      );
    } finally {
      setGeneratingReportId(null);
    }
  };

  // =========================================================
  // CURRENT REPORT
  // =========================================================

  const handleGenerateCurrentReport =
    () => {
      if (!result?.scan_id) {
        alert(
          "Scan ID is missing. Please analyze the image again."
        );
        return;
      }

      generateReport(
        result.scan_id,
        city
      );
    };

  // =========================================================
  // DELETE SINGLE SCAN
  // =========================================================

  const handleDeleteScan = async (
    scanId
  ) => {
    const confirmed =
      window.confirm(
        "Are you sure you want to delete this scan?"
      );

    if (!confirmed) {
      return;
    }

    setDeletingScanId(scanId);

    try {
      const response =
        await axios.delete(
          `${API_URL}/api/history/${scanId}`
        );

      if (
        response.data?.status ===
        "error"
      ) {
        throw new Error(
          response.data.message ||
            "Unable to delete scan."
        );
      }

      if (
        result?.scan_id === scanId
      ) {
        setResult(null);
        setLocalGuidance(null);
      }

      // Remove city selection for deleted scan.
      setHistoryCities((previous) => {
        const updated = {
          ...previous,
        };

        delete updated[scanId];

        return updated;
      });

      await loadDashboardData();
    } catch (error) {
      console.error(
        "Delete scan error:",
        error
      );

      alert(
        error.response?.data?.detail ||
          error.response?.data?.message ||
          error.message ||
          "Unable to delete the scan."
      );
    } finally {
      setDeletingScanId(null);
    }
  };

  // =========================================================
  // DELETE ALL
  // =========================================================

  const handleDeleteAllScans =
    async () => {
      if (history.length === 0) {
        return;
      }

      const confirmed =
        window.confirm(
          "Are you sure you want to delete ALL scan history? This cannot be undone."
        );

      if (!confirmed) {
        return;
      }

      setDeletingAll(true);

      try {
        const response =
          await axios.delete(
            `${API_URL}/api/history`
          );

        if (
          response.data?.status ===
          "error"
        ) {
          throw new Error(
            response.data.message ||
              "Unable to delete scan history."
          );
        }

        setHistory([]);

        setHistoryCities({});

        setStats({
          total_scans: 0,
          recyclable_scans: 0,
          non_recyclable_scans: 0,
          average_confidence: 0,
        });

        setResult(null);
        setLocalGuidance(null);
      } catch (error) {
        console.error(
          "Delete all scans error:",
          error
        );

        alert(
          error.response?.data?.detail ||
            error.response?.data?.message ||
            error.message ||
            "Unable to delete scan history."
        );
      } finally {
        setDeletingAll(false);
      }
    };

  // =========================================================
  // CONFIDENCE
  // =========================================================

  const getConfidenceClass = (
    confidence
  ) => {
    const value = Number(
      confidence || 0
    );

    if (value >= 70) {
      return "high";
    }

    if (value >= 45) {
      return "medium";
    }

    return "low";
  };

  const getConfidenceLabel = (
    confidence
  ) => {
    const value = Number(
      confidence || 0
    );

    if (value >= 70) {
      return "High";
    }

    if (value >= 45) {
      return "Medium";
    }

    return "Low";
  };

  // =========================================================
  // DATE
  // =========================================================

  const formatDate = (
    dateString
  ) => {
    if (!dateString) {
      return "—";
    }

    try {
      return new Date(
        dateString
      ).toLocaleString(
        "en-IN",
        {
          dateStyle: "medium",
          timeStyle: "short",
        }
      );
    } catch {
      return dateString;
    }
  };

  // =========================================================
  // CURRENT RESULT
  // =========================================================

  const analysis =
    result?.analysis;

  const classification =
    analysis?.classification;

  const recommendation =
    analysis?.recommendation;

  const confidence = Number(
    analysis?.confidence ||
      classification?.confidence ||
      0
  );

  const confidenceClass =
    getConfidenceClass(
      confidence
    );

  const confidenceLabel =
    analysis?.confidence_level ||
    getConfidenceLabel(
      confidence
    );

  const alternatives =
    analysis?.alternatives || [];

  // =========================================================
  // RECYCLABILITY
  // =========================================================

  const totalScans = Number(
    stats?.total_scans || 0
  );

  const recyclableScans =
    Number(
      stats?.recyclable_scans || 0
    );

  const nonRecyclableScans =
    Number(
      stats?.non_recyclable_scans ||
        0
    );

  const recyclablePercentage =
    totalScans > 0
      ? Math.round(
          (recyclableScans /
            totalScans) *
            100
        )
      : 0;

  // =========================================================
  // RENDER
  // =========================================================

  return (
    <div className="app">

      {/* ===================================================
          HEADER
      =================================================== */}

      <header className="top-header">

        <div className="brand">

          <div className="brand-icon">
            <Leaf size={22} />
          </div>

          <div>
            <div className="brand-name">
              EcoVision AI
            </div>

            <div className="brand-subtitle">
              Intelligent Waste Analysis
            </div>
          </div>

        </div>

        <div className="system-status">
          <span className="status-dot"></span>
          AI SYSTEM ONLINE
        </div>

      </header>

      <main className="main-container">

        {/* =================================================
            HERO
        ================================================= */}

        <section className="hero-section">

          <div className="section-label">
            <Sparkles size={14} />
            AI-POWERED WASTE INTELLIGENCE
          </div>

          <h1 className="hero-title">
            Understand Your Waste.
            <br />
            <span>
              Make Better Choices.
            </span>
          </h1>

          <p className="hero-description">
            Upload an image of household
            waste and EcoVision AI will
            identify the material, evaluate
            recyclability, recommend the
            correct disposal method, and
            provide city-specific disposal
            guidance.
          </p>

        </section>

        {/* =================================================
            UPLOAD
        ================================================= */}

        <section className="upload-container">

          {!selectedFile ? (
            <div
              className="upload-dropzone"
              onClick={() =>
                fileInputRef.current?.click()
              }
            >

              <div className="upload-icon">
                <Upload size={30} />
              </div>

              <h3>
                Upload Waste Image
              </h3>

              <p>
                Select an image of the waste
                you want EcoVision AI to
                analyze.
              </p>

              <button
                type="button"
                className="upload-button"
                onClick={(event) => {
                  event.stopPropagation();

                  fileInputRef.current?.click();
                }}
              >
                <FileImage size={17} />
                Choose Image
              </button>

              <span className="upload-hint">
                JPG, JPEG, PNG or WEBP
              </span>

            </div>
          ) : (
            <div className="selected-image-container">

              <div className="selected-image-preview-wrapper">

                <img
                  src={previewUrl}
                  alt="Selected waste"
                  className="selected-image-preview"
                />

              </div>

              <div className="selected-file-name">

                <FileImage size={17} />

                <span>
                  {selectedFile.name}
                </span>

              </div>

              <div className="image-action-buttons">

                <button
                  type="button"
                  className="change-image-button"
                  onClick={
                    handleChangeImage
                  }
                >
                  <RefreshCw size={16} />
                  Change Image
                </button>

                <button
                  type="button"
                  className="remove-image-button"
                  onClick={
                    handleRemoveImage
                  }
                >
                  <X size={16} />
                  Remove
                </button>

              </div>

              <button
                type="button"
                className="analyze-button"
                onClick={
                  handleAnalyze
                }
                disabled={analyzing}
              >

                {analyzing ? (
                  <>
                    <Loader2
                      size={19}
                      className="spin"
                    />
                    Analyzing Waste...
                  </>
                ) : (
                  <>
                    <Brain size={19} />
                    Analyze Waste
                    <ChevronRight size={18} />
                  </>
                )}

              </button>

            </div>
          )}

          <input
            ref={fileInputRef}
            type="file"
            accept="image/png,image/jpeg,image/jpg,image/webp"
            onChange={
              handleFileChange
            }
            style={{
              display: "none",
            }}
          />

          {uploadError && (
            <div className="error-message">

              <AlertCircle size={17} />

              <span>
                {uploadError}
              </span>

            </div>
          )}

        </section>

        {/* =================================================
            ANALYSIS RESULT
        ================================================= */}

        {result && analysis && (
          <section
            className="analysis-section"
            ref={analysisResultRef}
          >

            <div className="section-label">
              <Brain size={14} />
              AI ANALYSIS RESULT
            </div>

            <div className="analysis-title-row">

              <div>

                <h2 className="analysis-title">
                  Waste Detection
                </h2>

                <p className="analysis-subtitle">
                  EcoVision AI has analyzed
                  the uploaded image.
                </p>

              </div>

              <div
                className={`confidence-card ${confidenceClass}`}
              >

                <div className="confidence-label">
                  CONFIDENCE
                </div>

                <div className="confidence-value">
                  {confidence.toFixed(2)}%
                </div>

                <div className="confidence-level">
                  {confidenceLabel}
                </div>

              </div>

            </div>

            <div className="analysis-result-grid">

              <div className="analysis-image-card">

                <img
                  src={getImageUrl(
                    result.image_url
                  )}
                  alt="Analyzed waste"
                />

              </div>

              <div className="analysis-details-card">

                <div className="detected-label">
                  DETECTED WASTE
                </div>

                <h3>
                  {classification?.category ||
                    analysis?.waste_type ||
                    "Unknown Waste"}
                </h3>

                <div className="result-info-grid">

                  <div className="result-info-card">

                    <span>
                      Waste Type
                    </span>

                    <strong>
                      {classification?.waste_type ||
                        analysis?.waste_type ||
                        "—"}
                    </strong>

                  </div>

                  <div className="result-info-card">

                    <span>
                      Material
                    </span>

                    <strong>
                      {classification?.material ||
                        "—"}
                    </strong>

                  </div>

                  <div className="result-info-card">

                    <span>
                      Category
                    </span>

                    <strong>
                      {classification?.category ||
                        "—"}
                    </strong>

                  </div>

                  <div className="result-info-card">

                    <span>
                      Recyclable
                    </span>

                    <strong
                      className={
                        classification?.recyclable
                          ? "positive-text"
                          : "negative-text"
                      }
                    >
                      {classification?.recyclable
                        ? "Yes"
                        : "No"}
                    </strong>

                  </div>

                </div>

                {analysis?.confidence_message && (
                  <div className="confidence-message">

                    <ShieldCheck size={17} />

                    <span>
                      {
                        analysis.confidence_message
                      }
                    </span>

                  </div>
                )}

              </div>

            </div>

            {alternatives.length > 0 && (
              <div className="alternatives-card">

                <div className="card-heading">
                  <Activity size={17} />
                  Alternative Predictions
                </div>

                <div className="alternative-list">

                  {alternatives.map(
                    (item, index) => (
                      <div
                        className="alternative-item"
                        key={`${item.label}-${index}`}
                      >

                        <span>
                          {item.label}
                        </span>

                        <div className="alternative-score">

                          <div className="alternative-bar">

                            <div
                              className="alternative-bar-fill"
                              style={{
                                width: `${Math.min(
                                  Number(
                                    item.confidence ||
                                      0
                                  ),
                                  100
                                )}%`,
                              }}
                            />

                          </div>

                          <strong>
                            {Number(
                              item.confidence ||
                                0
                            ).toFixed(2)}
                            %
                          </strong>

                        </div>

                      </div>
                    )
                  )}

                </div>

              </div>
            )}

            {/* =================================================
                RESPONSIBLE DISPOSAL
            ================================================= */}

            <div className="recommendation-section">

              <div className="section-label">
                <Recycle size={14} />
                RESPONSIBLE DISPOSAL
              </div>

              <div className="recommendation-grid">

                <div className="recommendation-card">

                  <div className="recommendation-icon">
                    <Trash2 size={19} />
                  </div>

                  <div>

                    <span>
                      Recommended Bin
                    </span>

                    <strong>
                      {recommendation?.recommended_bin ||
                        "See disposal guidance"}
                    </strong>

                  </div>

                </div>

                <div className="recommendation-card">

                  <div className="recommendation-icon">
                    <Recycle size={19} />
                  </div>

                  <div>

                    <span>
                      Disposal Instruction
                    </span>

                    <strong>
                      {recommendation?.disposal_instruction ||
                        "Follow the recommended disposal method."}
                    </strong>

                  </div>

                </div>

                <div className="recommendation-card">

                  <div className="recommendation-icon">
                    <ShieldCheck size={19} />
                  </div>

                  <div>

                    <span>
                      Handling Instruction
                    </span>

                    <strong>
                      {recommendation?.handling_instruction ||
                        "Handle the material safely."}
                    </strong>

                  </div>

                </div>

                <div className="recommendation-card">

                  <div className="recommendation-icon">
                    <Leaf size={19} />
                  </div>

                  <div>

                    <span>
                      Eco Tip
                    </span>

                    <strong>
                      {recommendation?.eco_tip ||
                        "Reduce, reuse and recycle whenever possible."}
                    </strong>

                  </div>

                </div>

              </div>

            </div>

            {/* =================================================
                CURRENT RESULT REPORT
            ================================================= */}

            <button
              type="button"
              className="history-report-button"
              style={{
                marginTop: "20px",
                width: "100%",
                padding: "13px 18px",
              }}
              onClick={
                handleGenerateCurrentReport
              }
              disabled={
                generatingReportId ===
                result.scan_id
              }
            >

              <FileText size={17} />

              {generatingReportId ===
              result.scan_id
                ? "Generating PDF..."
                : `Generate Report — ${city}`}

            </button>

            {/* =================================================
                LOCAL DISPOSAL
            ================================================= */}

            <section className="local-disposal-section">

              <div className="section-label">
                <MapPin size={14} />
                LOCAL DISPOSAL INTELLIGENCE
              </div>

              <div className="local-disposal-header">

                <div>

                  <h2>
                    Disposal Guidance by City
                  </h2>

                  <p>
                    Get location-aware disposal
                    instructions for the detected
                    waste category.
                  </p>

                </div>

                <div className="city-selector">

                  <MapPin size={17} />

                  <select
                    value={city}
                    onChange={(event) => {
                      setCity(
                        event.target.value
                      );
                    }}
                  >

                    <option value="Indore">
                      Indore
                    </option>

                    <option value="Bhopal">
                      Bhopal
                    </option>

                    <option value="Delhi">
                      Delhi
                    </option>

                    <option value="Mumbai">
                      Mumbai
                    </option>

                  </select>

                </div>

              </div>

              <button
                type="button"
                className="local-guidance-button"
                onClick={() => {

                  const category =
                    result?.analysis
                      ?.classification
                      ?.category;

                  loadLocalGuidance(
                    category,
                    city
                  );

                }}
                disabled={
                  localLoading ||
                  !classification?.category
                }
              >

                {localLoading ? (
                  <>
                    <Loader2
                      size={17}
                      className="spin"
                    />
                    Loading Guidance...
                  </>
                ) : (
                  <>
                    <RefreshCw size={17} />
                    Refresh Local Guidance
                  </>
                )}

              </button>

              {localError && (
                <div className="error-message">

                  <AlertCircle size={17} />

                  <span>
                    {localError}
                  </span>

                </div>
              )}

              {!localLoading &&
                !localError &&
                localGuidance && (
                  <div className="local-guidance-card">

                    <div className="local-guidance-title">

                      <div className="local-guidance-icon">
                        <MapPin size={23} />
                      </div>

                      <div>

                        <span>
                          LOCAL GUIDANCE
                        </span>

                        <h3>
                          {localGuidance.city ||
                            city}
                        </h3>

                      </div>

                    </div>

                    <div className="local-guidance-content">

                      <div className="local-guidance-main">

                        <strong>
                          Recommended Action
                        </strong>

                        <p>
                          {localGuidance.local_instruction ||
                            "Follow the recommended local disposal process."}
                        </p>

                      </div>

                      <div className="local-guidance-note">

                        <CircleAlert
                          size={17}
                        />

                        <p>
                          {localGuidance.important_note ||
                            "Local collection schedules, authorized facilities and municipal rules can change. Verify the latest guidance from the relevant municipal authority before disposal."}
                        </p>

                      </div>

                    </div>

                  </div>
                )}

              {!localLoading &&
                !localError &&
                !localGuidance && (
                  <div className="local-empty-state">

                    <MapPin size={18} />

                    <span>
                      Select a city to view
                      local disposal guidance.
                    </span>

                  </div>
                )}

            </section>

          </section>
        )}

        {/* =================================================
            DASHBOARD
        ================================================= */}

        <section className="dashboard-section">

          <div className="section-label">
            <BarChart3 size={14} />
            ECO ANALYTICS
          </div>

          <div className="dashboard-header">

            <div>

              <h2>
                Your Waste Dashboard
              </h2>

              <p>
                Overview of your EcoVision AI
                analysis activity.
              </p>

            </div>

            <button
              type="button"
              className="dashboard-refresh-button"
              onClick={
                loadDashboardData
              }
              disabled={
                dashboardLoading
              }
            >

              {dashboardLoading ? (
                <Loader2
                  size={16}
                  className="spin"
                />
              ) : (
                <RefreshCw size={16} />
              )}

              Refresh

            </button>

          </div>

          <div className="stats-grid">

            <div className="stat-card">

              <div className="stat-icon">
                <Activity size={20} />
              </div>

              <div>

                <span>
                  Total Scans
                </span>

                <strong>
                  {totalScans}
                </strong>

              </div>

            </div>

            <div className="stat-card">

              <div className="stat-icon">
                <Recycle size={20} />
              </div>

              <div>

                <span>
                  Recyclable
                </span>

                <strong>
                  {recyclableScans}
                </strong>

              </div>

            </div>

            <div className="stat-card">

              <div className="stat-icon">
                <Trash2 size={20} />
              </div>

              <div>

                <span>
                  Non-Recyclable
                </span>

                <strong>
                  {nonRecyclableScans}
                </strong>

              </div>

            </div>

            <div className="stat-card">

              <div className="stat-icon">
                <Brain size={20} />
              </div>

              <div>

                <span>
                  Avg. Confidence
                </span>

                <strong>
                  {Number(
                    stats.average_confidence ||
                      0
                  ).toFixed(2)}
                  %
                </strong>

              </div>

            </div>

          </div>

          <div className="analytics-grid">

            <div className="analytics-card">

              <div className="card-heading">
                <Recycle size={17} />
                Recyclability Overview
              </div>

              <div className="recyclability-wrapper">

                <div
                  className="recyclability-circle"
                  style={{
                    "--progress":
                      `${recyclablePercentage}%`,
                  }}
                >

                  <div>

                    <strong>
                      {recyclablePercentage}%
                    </strong>

                    <span>
                      Recyclable
                    </span>

                  </div>

                </div>

                <div className="recyclability-info">

                  <p>
                    <strong>
                      {recyclableScans}
                    </strong>{" "}
                    of{" "}
                    <strong>
                      {totalScans}
                    </strong>{" "}
                    analyzed items are
                    classified as recyclable.
                  </p>

                </div>

              </div>

            </div>

            <div className="analytics-card">

              <div className="card-heading">
                <ShieldCheck size={17} />
                AI Performance
              </div>

              <div className="performance-list">

                <div className="performance-row">

                  <span>
                    Average Confidence
                  </span>

                  <strong>
                    {Number(
                      stats.average_confidence ||
                        0
                    ).toFixed(2)}
                    %
                  </strong>

                </div>

                <div className="performance-row">

                  <span>
                    Total Analyses
                  </span>

                  <strong>
                    {totalScans}
                  </strong>

                </div>

                <div className="performance-row">

                  <span>
                    Recyclable Rate
                  </span>

                  <strong>
                    {recyclablePercentage}%
                  </strong>

                </div>

              </div>

            </div>

          </div>

        </section>

        {/* =================================================
            HISTORY
        ================================================= */}

        <section className="history-section">

          <div className="section-label">
            <Activity size={14} />
            SCAN HISTORY
          </div>

          <div className="history-header">

            <div>

              <h2>
                Recent Analyses
              </h2>

              <p>
                Review previous waste
                classifications and reports.
              </p>

            </div>

            {history.length > 0 && (
              <button
                type="button"
                className="history-delete-button"
                onClick={
                  handleDeleteAllScans
                }
                disabled={deletingAll}
              >

                {deletingAll ? (
                  <Loader2
                    size={15}
                    className="spin"
                  />
                ) : (
                  <Trash2 size={15} />
                )}

                {deletingAll
                  ? "Deleting..."
                  : "Delete All"}

              </button>
            )}

          </div>

          {history.length === 0 ? (
            <div className="history-empty-state">

              <Activity size={28} />

              <h3>
                No scan history yet
              </h3>

              <p>
                Analyze your first waste
                image to start building
                your history.
              </p>

            </div>
          ) : (
            <div className="history-list">

              {history.map((scan) => {

                /*
                 * If this scan doesn't have a city
                 * selected yet, use the current main
                 * city as its initial value.
                 */
                const historyCity =
                  historyCities[scan.id] ||
                  city;

                return (
                  <div
                    className="history-item"
                    key={scan.id}
                  >

                    {/* IMAGE */}

                    <div className="history-image">

                      {scan.stored_filename ? (
                        <img
                          src={getImageUrl(
                            `/uploads/${scan.stored_filename}`
                          )}
                          alt={
                            scan.category ||
                            "Waste"
                          }
                        />
                      ) : (
                        <FileImage
                          size={24}
                        />
                      )}

                    </div>

                    {/* MAIN */}

                    <div className="history-main">

                      <div className="history-top-row">

                        <div>

                          <h3>
                            {scan.category ||
                              scan.waste_type ||
                              "Unknown Waste"}
                          </h3>

                          <p>
                            {scan.material ||
                              "Unknown material"}
                          </p>

                        </div>

                        <div className="history-confidence">
                          {Number(
                            scan.confidence ||
                              0
                          ).toFixed(2)}
                          %
                        </div>

                      </div>

                      <div className="history-meta">

                        <span>
                          {scan.recyclable
                            ? "Recyclable"
                            : "Non-Recyclable"}
                        </span>

                        <span>
                          {formatDate(
                            scan.created_at
                          )}
                        </span>

                        <span>
                          Scan #{scan.id}
                        </span>

                      </div>

                      {/* =================================================
                          HISTORY ACTIONS + CITY
                      ================================================= */}

                      <div className="history-actions">

                        {/* INDIVIDUAL CITY SELECTOR */}

                        <div
                          style={{
                            display: "inline-flex",
                            alignItems: "center",
                            gap: "7px",
                            padding: "8px 11px",
                            borderRadius: "9px",
                            border:
                              "1px solid rgba(71, 214, 125, 0.18)",
                            background:
                              "rgba(29, 126, 65, 0.08)",
                            color: "#52e989",
                          }}
                        >

                          <MapPin
                            size={14}
                          />

                          <select
                            value={
                              historyCity
                            }
                            onChange={(
                              event
                            ) => {
                              setHistoryCities(
                                (previous) => ({
                                  ...previous,
                                  [scan.id]:
                                    event
                                      .target
                                      .value,
                                })
                              );
                            }}
                            style={{
                              border: "none",
                              outline: "none",
                              background:
                                "transparent",
                              color:
                                "#bce5c9",
                              fontSize:
                                "11px",
                              fontWeight:
                                700,
                              cursor:
                                "pointer",
                            }}
                          >

                            <option
                              value="Indore"
                              style={{
                                background:
                                  "#0a2417",
                                color:
                                  "#ffffff",
                              }}
                            >
                              Indore
                            </option>

                            <option
                              value="Bhopal"
                              style={{
                                background:
                                  "#0a2417",
                                color:
                                  "#ffffff",
                              }}
                            >
                              Bhopal
                            </option>

                            <option
                              value="Delhi"
                              style={{
                                background:
                                  "#0a2417",
                                color:
                                  "#ffffff",
                              }}
                            >
                              Delhi
                            </option>

                            <option
                              value="Mumbai"
                              style={{
                                background:
                                  "#0a2417",
                                color:
                                  "#ffffff",
                              }}
                            >
                              Mumbai
                            </option>

                          </select>

                        </div>

                        {/* REPORT */}

                        <button
                          type="button"
                          className="history-report-button"
                          onClick={() =>
                            generateReport(
                              scan.id,
                              historyCity
                            )
                          }
                          disabled={
                            generatingReportId ===
                            scan.id
                          }
                        >

                          <FileText
                            size={15}
                          />

                          {generatingReportId ===
                          scan.id
                            ? "Generating..."
                            : `Report — ${historyCity}`}

                        </button>

                        {/* DELETE */}

                        <button
                          type="button"
                          className="history-delete-button"
                          onClick={() =>
                            handleDeleteScan(
                              scan.id
                            )
                          }
                          disabled={
                            deletingScanId ===
                            scan.id
                          }
                        >

                          {deletingScanId ===
                          scan.id ? (
                            <Loader2
                              size={15}
                              className="spin"
                            />
                          ) : (
                            <Trash2
                              size={15}
                            />
                          )}

                          {deletingScanId ===
                          scan.id
                            ? "Deleting..."
                            : "Delete"}

                        </button>

                      </div>

                    </div>

                  </div>
                );
              })}

            </div>
          )}

        </section>

        {/* =================================================
            FOOTER
        ================================================= */}

        <footer className="app-footer">

          <div className="footer-brand">

            <Leaf size={16} />

            <span>
              EcoVision AI
            </span>

          </div>

          <p>
            AI-powered waste intelligence
            for smarter and more responsible
            disposal.
          </p>

          <span className="footer-status">
            Local AI • Privacy Focused •
            Eco-Friendly
          </span>

        </footer>

      </main>
    </div>
  );
}

export default App;