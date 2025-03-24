import { CanvasModel, CanvasView } from '../widget';
import { createTestModel } from './utils';


describe('CanvasModel', () => {
  it('should be createable with default values', () => {
    const model = createTestModel(CanvasModel);
    expect(model).toBeInstanceOf(CanvasModel);
    expect(model.get('width')).toBe(28);
    expect(model.get('height')).toBe(28);
    expect(model.get('zoom')).toBe(8.0);
    expect(model.get('base64_data')).toBe('');
  });

  it('should be createable with custom values', () => {
    const state = { width: 64, height: 48, zoom: 4.0 };
    const model = createTestModel(CanvasModel, state);
    expect(model.get('width')).toBe(64);
    expect(model.get('height')).toBe(48);
    expect(model.get('zoom')).toBe(4.0);
  });

  it('should update attributes properly', () => {
    const model = createTestModel(CanvasModel);
    model.set('width', 100);
    model.set('height', 75);
    model.set('zoom', 2.0);
    expect(model.get('width')).toBe(100);
    expect(model.get('height')).toBe(75);
    expect(model.get('zoom')).toBe(2.0);
  });

  it('should have proper serializers', () => {
    expect(CanvasModel.serializers.image_data).toBeDefined();
    const testBytes = new Uint8Array([255, 0, 0, 255]);
    const model = createTestModel(CanvasModel, { image_data: testBytes });
    expect(model.get('image_data')).toEqual(testBytes);
  });

  it('should have correct static properties', () => {
    expect(CanvasModel.model_name).toBe('CanvasModel');
    expect(CanvasModel.view_name).toBe('CanvasView');
  });
});

describe('CanvasView', () => {
  let model: CanvasModel;
  let view: CanvasView;

  beforeEach(() => {
    model = createTestModel(CanvasModel);
    view = new CanvasView({ model });
    document.body.appendChild(view.el);
  });

  afterEach(() => {
    document.body.removeChild(view.el);
  });

  it('should render canvas and wrapper', () => {
    view.render();
    expect(view.el.querySelector('canvas')).toBeTruthy();
    expect(view.el.querySelector('div')).toBeTruthy();
  });

  it('should update canvas size on model change', () => {
    view.render();
    model.set('width', 100);
    model.set('height', 75);
    expect(view.canvas.width).toBe(100);
    expect(view.canvas.height).toBe(75);
  });

  it('should update zoom styles', () => {
    view.render();
    model.set('zoom', 4.0);
    expect(view.canvas.style.width).toBe('112px');
    expect(view.canvas.style.height).toBe('112px');
  });

  it('should render grid overlay when zoom is large enough', () => {
    view.render();
    model.set('zoom', 5.0);
    expect(view.canvasWrapper.querySelector('.ipypencil-grid')).toBeTruthy();
  });

  it('should handle mouse drawing events', () => {
    view.render();
    const canvas = view.canvas;
    const ctx = view.ctx;
    const spy = jest.spyOn(ctx, 'stroke');

    canvas.dispatchEvent(new MouseEvent('mousedown', { clientX: 10, clientY: 10 }));
    canvas.dispatchEvent(new MouseEvent('mousemove', { clientX: 20, clientY: 20 }));
    canvas.dispatchEvent(new MouseEvent('mouseup'));

    expect(spy).toHaveBeenCalled();
  });

  it('should handle touch drawing events', () => {
    view.render();
    const canvas = view.canvas;
    const ctx = view.ctx;
    const spy = jest.spyOn(ctx, 'stroke');

    canvas.dispatchEvent(new TouchEvent('touchstart', { touches: [{ clientX: 10, clientY: 10 } as Touch] }));
    canvas.dispatchEvent(new TouchEvent('touchmove', { touches: [{ clientX: 20, clientY: 20 } as Touch] }));
    canvas.dispatchEvent(new TouchEvent('touchend'));

    expect(spy).toHaveBeenCalled();
  });

  it('should clear the canvas on custom message', () => {
    view.render();
    const ctx = view.ctx;
    const spy = jest.spyOn(ctx, 'fillRect');

    view.onCustomMessage({ action: 'clear' });
    expect(spy).toHaveBeenCalledWith(0, 0, view.canvas.width, view.canvas.height);
  });

  it('should update image data on custom message', () => {
    view.render();
    const spy = jest.spyOn(view, 'updateImageData');
    view.onCustomMessage({ action: 'update_image_data' });
    expect(spy).toHaveBeenCalled();
  });
});