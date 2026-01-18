function ModelSelector({ modelSize, setModelSize }) {
  return (
    <div className="control-group">
      <label>Model Complexity</label>
      <select
        value={modelSize}
        onChange={(e) => setModelSize(e.target.value)}
      >
        <option value="n">Nano (Fast)</option>
        <option value="s">Small</option>
        <option value="m">Medium</option>
        <option value="l">Large (Accurate)</option>
      </select>
    </div>
  );
}

export default ModelSelector;
