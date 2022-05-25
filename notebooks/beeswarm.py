import numpy as np
from shap.plots import colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as plt
import plot_init as pu
import matplotlib as mpl

def beeswarm(features, shap_values, ax, color_bar=True, axis_color="#333333",
             cmap=colors.red_blue, row_height=0.4, alpha=1, max_display=20,
             markersize=5, reverse_order=True):
    feature_names = features.columns
    # feature index to category flag
    idx2cat = features.dtypes.astype(str).isin(["object", "category"]).tolist()
    features = features.values

    feature_order = np.argsort(np.sum(np.abs(shap_values), axis=0))
    if reverse_order:
        feature_order = feature_order[::-1]
    feature_order = feature_order[-min(max_display, len(feature_order)):]
    ax.axvline(x=0, color="#999999", zorder=-1, lw=0.7)
    for pos, i in enumerate(feature_order):
        ax.axhline(y=pos, color="#cccccc", lw=0.5, dashes=(1, 5), zorder=-1)
        shaps = shap_values[:, i]
        values = None if features is None else features[:, i]
        inds = np.arange(len(shaps))
        np.random.shuffle(inds)
        if values is not None:
            values = values[inds]
        shaps = shaps[inds]
        colored_feature = True
        try:
            if idx2cat is not None and idx2cat[i]:  # check categorical feature
                colored_feature = False
            else:
                # make sure this can be numeric
                values = np.array(values, dtype=np.float64)
        except:
            colored_feature = False
        N = len(shaps)
        nbins = 100
        quant = np.round(nbins * (shaps - np.min(shaps)) /
                         (np.max(shaps) - np.min(shaps) + 1e-8))
        inds = np.argsort(quant + np.random.randn(N) * 1e-6)
        layer = 0
        last_bin = -1
        ys = np.zeros(N)
        for ind in inds:
            if quant[ind] != last_bin:
                layer = 0
            ys[ind] = np.ceil(layer / 2) * ((layer % 2) * 2 - 1)
            layer += 1
            last_bin = quant[ind]
        ys *= 0.9 * (row_height / np.max(ys + 1))

        if features is not None and colored_feature:
            # trim the color range, but prevent the color range from collapsing
            vmin = np.nanpercentile(values, 5)
            vmax = np.nanpercentile(values, 95)
            if vmin == vmax:
                vmin = np.nanpercentile(values, 1)
                vmax = np.nanpercentile(values, 99)
                if vmin == vmax:
                    vmin = np.min(values)
                    vmax = np.max(values)
            if vmin > vmax:  # fixes rare numerical precision issues
                vmin = vmax

            assert features.shape[0] == len(
                shaps), "Feature and SHAP matrices must have the same number of rows!"

            # plot the nan values in the interaction feature as grey
            nan_mask = np.isnan(values)
            ax.scatter(shaps[nan_mask], pos + ys[nan_mask], color="#777777", vmin=vmin,
                       vmax=vmax, s=markersize, alpha=alpha, linewidth=0,
                       zorder=3, rasterized=len(shaps) > 500)

            # plot the non-nan values colored by the trimmed feature value
            cvals = values[np.invert(nan_mask)].astype(np.float64)
            cvals_imp = cvals.copy()
            cvals_imp[np.isnan(cvals)] = (vmin + vmax) / 2.0
            cvals[cvals_imp > vmax] = vmax
            cvals[cvals_imp < vmin] = vmin
            ax.scatter(shaps[np.invert(nan_mask)], pos + ys[np.invert(nan_mask)],
                       cmap=cmap, vmin=vmin, vmax=vmax, s=markersize,
                       c=cvals, alpha=alpha, linewidth=0,
                       zorder=3, rasterized=len(shaps) > 500)

    # draw the color bar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="1%", pad="3%")
    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([0, 1])
    fig = ax.get_figure()
    cb = fig.colorbar(sm, cax=cax, ticks=[0, 1])
    cb.set_ticklabels(['low', 'high'], size=pu.tiny)
    cb.set_label('feature value', size=pu.tiny, labelpad=0)
    cb.ax.tick_params(labelsize=pu.small, length=0)
    cb.set_alpha(1)
    cb.outline.set_visible(False)

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('none')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(color=axis_color, labelcolor=axis_color)

    ax.set_yticks(range(len(feature_order)), [
                  feature_names[i] for i in feature_order], fontsize=pu.small)
    ax.tick_params('y', length=20, width=0.5, which='major')
    ax.tick_params('x', labelsize=pu.small)
    ax.set_ylim(-1, len(feature_order))

    ax.set_xlabel("SHAP")
